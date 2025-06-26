from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class DataGenerator(ABC):
    """Abstract base class for data generation using various LLM APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    @abstractmethod
    def generate_data(self, requirement: str, num_records: int) -> List[Dict[str, Any]]:
        """Generate synthetic data based on user requirement.
        
        Args:
            requirement: Natural language description of data requirements
            num_records: Number of records to generate
            
        Returns:
            List of generated data records
        """
        pass
    
    def _convert_requirement_to_prompts(self, requirement: str, num_records: int) -> List[str]:
        """Convert user requirement to specific data generation prompts.
        
        Args:
            requirement: Natural language data requirement
            num_records: Number of records to generate
            
        Returns:
            List of specific prompts for each record
        """
        # Enhanced prompt with better instructions for synthetic data generation
        base_prompt = f"""You are a synthetic data generator. Generate
            realistic synthetic data based on this requirement:
            {requirement}

            Instructions:
            - Return only valid JSON without any additional text, explanations,
            or markdown formatting
            - The JSON should represent a single data record that matches the requirement
            - Ensure the data is realistic and varied
            - Use appropriate data types (strings, numbers, booleans, arrays, objects as needed)
            - Make each record unique and realistic

            Generate one data record now:
        """
        
        # Add slight variations to prompts to encourage diversity
        prompts = []
        for i in range(num_records):
            if i == 0:
                prompts.append(base_prompt)
            else:
                variation_prompt = base_prompt + f"\n\nMake this record distinct from previous records (this is record #{i+1})."
                prompts.append(variation_prompt)
        
        return prompts