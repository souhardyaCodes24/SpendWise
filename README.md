# SpendWise - AI-Powered Personal Finance Tracker

A production-ready Flask application that analyzes bank statement CSVs using AI to categorize transactions and provide personalized financial advice.

## Features

- 🤖 **AI-Powered Categorization**: Automatically categorizes transactions using Hugging Face transformers
- 📊 **Visual Analytics**: Interactive charts and spending breakdowns with Chart.js
- 💡 **Smart Recommendations**: Personalized savings advice powered by Google's Gemini AI
- 🎨 **Modern Dark UI**: Bolt-inspired design with glassmorphism effects
- 📱 **Fully Responsive**: Optimized for desktop and mobile devices
- ⚡ **Real-time Processing**: Fast CSV parsing and analysis

## Screenshots

*Upload Page*: Clean, intuitive drag-and-drop interface for CSV files
*Dashboard*: Comprehensive financial insights with interactive charts and AI recommendations

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Modern web browser

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd spendwise
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root or set the environment variable:
   ```bash
   # Option 1: Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   
   # Option 2: Set environment variable directly
   # Windows
   set GEMINI_API_KEY=your_gemini_api_key_here
   
   # macOS/Linux
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Getting a Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key to your environment variable

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Upload your CSV file**
   - Your CSV must have exactly 3 columns: `Date`, `Description`, `Amount`
   - Use the sample file in `examples/sample_transactions.csv` to test
   - Drag and drop or click to select your file

4. **View your financial insights**
   - AI-categorized transactions
   - Interactive spending chart
   - Personalized savings recommendations
   - Detailed transaction table

## CSV Format Requirements

Your bank statement CSV must have these exact column headers:

```csv
Date,Description,Amount
2024-01-02,Grocery Store Purchase,-85.43
2024-01-03,Netflix Subscription,-15.99
2024-01-05,Gas Station Fill Up,-42.50
```

- **Date**: Any standard date format (YYYY-MM-DD recommended)
- **Description**: Transaction description for AI categorization
- **Amount**: Negative values for expenses, positive for income

## Transaction Categories

The AI automatically categorizes transactions into:

- 🍔 **Food**: Restaurants, groceries, coffee shops
- 🏠 **Rent**: Housing payments, mortgage
- ⚡ **Utilities**: Electric, gas, water, internet, phone bills
- 🛍️ **Shopping**: Retail purchases, online orders
- 🚗 **Transport**: Gas, parking, rides, public transport
- 🎬 **Entertainment**: Movies, games, streaming services
- 📱 **Subscriptions**: Monthly/annual service payments
- 📦 **Other**: Miscellaneous expenses

## Project Structure

```
spendwise/
├── app.py                 # Main Flask application
├── models.py              # Hugging Face integration
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with navigation
│   ├── upload.html       # CSV upload page
│   └── dashboard.html    # Results dashboard
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Dark theme styling
│   └── js/
│       ├── main.js       # Common functionality
│       ├── upload.js     # Upload page interactions
│       └── dashboard.js  # Chart.js initialization
└── examples/
    └── sample_transactions.csv  # Test data
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Required for AI-powered recommendations
- `FLASK_ENV`: Set to `development` for debug mode

### Application Settings

Edit `app.py` to customize:

- `MAX_CONTENT_LENGTH`: File upload size limit (default: 16MB)
- `SECRET_KEY`: Change for production deployment
- Model selection in `models.py`

## API Integration

### Hugging Face

Uses `facebook/bart-large-mnli` for zero-shot transaction classification. The model automatically downloads on first use.

### Google Gemini

Sends aggregated spending data to Gemini for personalized advice. No individual transaction details are shared.

## Troubleshooting

### Common Issues

1. **"No module named 'transformers'"**
   ```bash
   pip install transformers torch
   ```

2. **"GEMINI_API_KEY not found"**
   - Verify your API key is set correctly
   - Check for typos in the environment variable name

3. **CSV validation errors**
   - Ensure exactly 3 columns: Date, Description, Amount
   - Check for proper CSV formatting
   - Use the sample file to test

4. **Slow first load**
   - Hugging Face model downloads on first use (~500MB)
   - Subsequent loads will be much faster

### Performance Tips

- Use SSD storage for faster model loading
- Ensure stable internet connection for API calls
- Consider using GPU acceleration for large datasets

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Consider rate limiting for production deployment
- Validate all user inputs

## Development

### Adding New Features

1. **New transaction categories**: Edit `models.py` categories list
2. **Custom styling**: Modify `static/css/style.css`
3. **Additional charts**: Extend `static/js/dashboard.js`

### Testing

Use the provided sample CSV file:
```bash
# Upload examples/sample_transactions.csv through the web interface
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production`
2. Use a proper WSGI server (Gunicorn, uWSGI)
3. Configure reverse proxy (Nginx)
4. Set up SSL/TLS certificates
5. Implement proper logging and monitoring

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your CSV format matches requirements
3. Ensure all dependencies are installed correctly
4. Test with the provided sample data first

## Acknowledgments

- **Hugging Face** for the BART model
- **Google** for the Gemini API
- **Chart.js** for visualization library
- **Flask** for the web framework

---

Built with ❤️ using AI and modern web technologies.
