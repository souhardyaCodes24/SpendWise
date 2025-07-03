"""
SpendWise - Personal Finance Tracker
A Flask application for CSV upload, transaction categorization, and AI-driven budgeting tips.
"""

import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai
from datetime import datetime
import json
import re
from models import TransactionCategorizer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AIzaSyBqln035JyrtPmrBVO_sa7hHErvBfEmsKE'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Add custom Jinja2 filter for line breaks
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks."""
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')

# Add custom Jinja2 filter for markdown parsing
@app.template_filter('parse_markdown')
def parse_markdown_filter(text):
    """Parse markdown text and remove headers while keeping formatting."""
    if text is None:
        return ''
    
    # Remove headers (lines starting with #)
    lines = text.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip header lines (starting with #)
        if line.strip().startswith('#'):
            continue
        filtered_lines.append(line)
    
    # Join back the lines
    text = '\n'.join(filtered_lines)
    
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Convert line breaks to <br>
    text = text.replace('\n', '<br>\n')
    
    return text

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the transaction categorizer
categorizer = TransactionCategorizer()

# Configure Gemini API
genai.configure(api_key="AIzaSyBqln035JyrtPmrBVO_sa7hHErvBfEmsKE")

def allowed_file(filename):
    """Check if uploaded file is a CSV file."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def validate_csv_structure(df):
    """
    Validate that the CSV has exactly three columns: Date, Description, Amount.
    
    Args:
        df (pd.DataFrame): The uploaded CSV data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_columns = ['Date', 'Description', 'Amount']
    
    if len(df.columns) != 3:
        return False, f"CSV must have exactly 3 columns. Found {len(df.columns)} columns."
    
    # Check if columns match required names (case-insensitive)
    df_columns = [col.strip().lower() for col in df.columns]
    required_lower = [col.lower() for col in required_columns]
    
    if df_columns != required_lower:
        return False, f"CSV columns must be: {', '.join(required_columns)}. Found: {', '.join(df.columns)}"
    
    # Check for empty data
    if df.empty:
        return False, "CSV file is empty."
    
    # Rename columns to standard format
    df.columns = required_columns
    
    # Validate data types
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
    except Exception as e:
        return False, f"Invalid data format: {str(e)}"
    
    return True, None

def process_transactions(df):
    """
    Process transactions: normalize descriptions and categorize using Hugging Face.
    
    Args:
        df (pd.DataFrame): DataFrame with Date, Description, Amount columns
        
    Returns:
        pd.DataFrame: Processed DataFrame with Category column added
    """
    # Normalize descriptions
    df['Description'] = df['Description'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    
    # Categorize transactions
    descriptions = df['Description'].tolist()
    categories = categorizer.categorize_transactions(descriptions)
    df['Category'] = categories
    
    return df

def generate_spending_summary(df):
    """
    Generate spending summary for Gemini API.
    
    Args:
        df (pd.DataFrame): Processed transactions DataFrame
        
    Returns:
        dict: Spending summary with category totals and monthly breakdown
    """
    # Calculate category totals
    category_totals = df.groupby('Category')['Amount'].sum().abs().to_dict()
    
    # Calculate monthly totals
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_totals = df.groupby('Month')['Amount'].sum().abs().to_dict()
    
    # Convert Period objects to strings for JSON serialization
    monthly_totals = {str(k): v for k, v in monthly_totals.items()}
    
    return {
        'category_totals': category_totals,
        'monthly_totals': monthly_totals,
        'total_spending': df['Amount'].sum()
    }

def get_gemini_advice(spending_summary):
    """
    Get personalized savings advice from Gemini API.
    
    Args:
        spending_summary (dict): Spending summary data
        
    Returns:
        str: AI-generated advice or error message
    """
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Create detailed analysis of spending patterns
        category_breakdown = ", ".join([f"{cat}: ${amount:.2f}" for cat, amount in spending_summary['category_totals'].items()])
        
        # Find highest spending categories
        sorted_categories = sorted(spending_summary['category_totals'].items(), key=lambda x: x[1], reverse=True)
        top_category = sorted_categories[0] if sorted_categories else ("Unknown", 0)
        second_category = sorted_categories[1] if len(sorted_categories) > 1 else ("Unknown", 0)
        
        # Calculate percentages
        total = abs(spending_summary['total_spending'])
        top_percentage = (top_category[1] / total * 100) if total > 0 else 0
        
        # Enhanced prompt with more context and specific requirements
        prompt = f"""
        You are a personal financial advisor analyzing spending patterns. Here's the complete financial overview:
        
        SPENDING BREAKDOWN:
        {category_breakdown}
        
        TOTAL SPENDING: ${total:.2f}
        TOP SPENDING CATEGORY: {top_category[0]} (${top_category[1]:.2f} - {top_percentage:.1f}% of total)
        SECOND HIGHEST: {second_category[0]} (${second_category[1]:.2f})
        
        ANALYSIS REQUIREMENTS:
        1. Provide exactly 3 specific, actionable money-saving recommendations
        2. Focus primarily on the highest spending categories
        3. Include specific dollar amounts or percentage targets where possible
        4. Make suggestions realistic and practical for everyday implementation
        5. Consider both immediate cost-cutting and long-term financial habits
        
        FORMAT REQUIREMENTS:
        - Use numbered list (1., 2., 3.)
        - Each tip should be 2-3 sentences maximum
        - Include specific actions the user can take this week
        - Mention potential savings amounts when possible
        
        Focus on practical advice that can lead to measurable savings based on the spending patterns shown.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Unable to generate advice at this time. Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and processing."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read CSV file
                df = pd.read_csv(file)
                
                # Validate CSV structure
                is_valid, error_message = validate_csv_structure(df)
                if not is_valid:
                    flash(error_message)
                    return redirect(request.url)
                
                # Process transactions
                processed_df = process_transactions(df)
                
                # Generate spending summary
                spending_summary = generate_spending_summary(processed_df)
                
                # Get AI advice
                advice = get_gemini_advice(spending_summary)
                
                # Prepare data for template
                transactions = processed_df.to_dict('records')
                for transaction in transactions:
                    transaction['Date'] = transaction['Date'].strftime('%Y-%m-%d')
                    transaction['Amount'] = f"${transaction['Amount']:.2f}"
                
                # Prepare chart data
                chart_data = {
                    'labels': list(spending_summary['category_totals'].keys()),
                    'data': list(spending_summary['category_totals'].values())
                }
                
                return render_template('dashboard.html', 
                                     transactions=transactions,
                                     chart_data=chart_data,
                                     advice=advice,
                                     spending_summary=spending_summary)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Please upload a valid CSV file')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash("File is too large. Maximum size is 16MB.")
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
