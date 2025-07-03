"""
Transaction categorization using Hugging Face transformers.
"""

from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionCategorizer:
    """
    A class to categorize financial transactions using Hugging Face zero-shot classification.
    """
    
    def __init__(self):
        """Initialize the categorizer with predefined categories and model."""
        self.categories = [
            "Food",
            "Rent", 
            "Utilities",
            "Shopping",
            "Transport",
            "Entertainment",
            "Subscriptions",
            "Other"
        ]
        
        # Initialize the zero-shot classification pipeline
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU (-1) or GPU (0)
            )
            logger.info("Transaction categorizer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize categorizer: {e}")
            self.classifier = None
    
    def categorize_single_transaction(self, description):
        """
        Categorize a single transaction description.
        
        Args:
            description (str): The transaction description
            
        Returns:
            str: The predicted category
        """
        if not self.classifier:
            return "Other"
            
        try:
            # Clean the description
            description = str(description).strip()
            if not description:
                return "Other"
            
            # Use zero-shot classification
            result = self.classifier(description, self.categories)
            
            # Return the category with highest confidence
            return result['labels'][0]
            
        except Exception as e:
            logger.error(f"Error categorizing transaction '{description}': {e}")
            return "Other"
    
    def categorize_transactions(self, descriptions):
        """
        Categorize multiple transaction descriptions.
        
        Args:
            descriptions (list): List of transaction descriptions
            
        Returns:
            list: List of predicted categories
        """
        if not self.classifier:
            logger.warning("Classifier not available, returning 'Other' for all transactions")
            return ["Other"] * len(descriptions)
        
        categories = []
        
        for desc in descriptions:
            category = self.categorize_single_transaction(desc)
            categories.append(category)
            
        logger.info(f"Categorized {len(descriptions)} transactions")
        return categories
    
    def get_category_rules(self):
        """
        Get rule-based categorization for common transaction patterns.
        This serves as a fallback if the ML model fails.
        
        Returns:
            dict: Dictionary mapping keywords to categories
        """
        return {
            'Food': ['restaurant', 'food', 'grocery', 'cafe', 'coffee', 'pizza', 'burger', 'takeout', 'delivery', 'dining'],
            'Rent': ['rent', 'mortgage', 'housing', 'apartment', 'landlord'],
            'Utilities': ['electric', 'gas', 'water', 'internet', 'phone', 'utility', 'bill', 'power'],
            'Shopping': ['amazon', 'target', 'walmart', 'shopping', 'store', 'retail', 'purchase', 'buy'],
            'Transport': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'bus', 'train', 'parking', 'car', 'transportation'],
            'Entertainment': ['movie', 'cinema', 'theater', 'concert', 'game', 'entertainment', 'fun', 'hobby'],
            'Subscriptions': ['subscription', 'netflix', 'spotify', 'premium', 'monthly', 'annual', 'service'],
            'Other': []
        }
    
    def rule_based_categorization(self, description):
        """
        Fallback rule-based categorization using keyword matching.
        
        Args:
            description (str): The transaction description
            
        Returns:
            str: The predicted category
        """
        description = str(description).lower()
        rules = self.get_category_rules()
        
        for category, keywords in rules.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return "Other"
