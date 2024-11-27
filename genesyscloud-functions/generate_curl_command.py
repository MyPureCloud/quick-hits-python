# >> START generate-curl-command-py
import json
import sys
import logging
import argparse
from typing import Any, Optional

"""
Generate Curl Command Script
---------------------------

A utility script that generates formatted curl commands for uploading ZIP files 
to AWS S3 with specific metadata headers.

Core Functionality:
    - Reads and parses JSON data from standard input (STDIN)
    - Generates a curl command for uploading ZIP files with AWS S3 metadata headers

Classes:
    JsonParser:
        Methods:
        - parse_json_from_stdin(): Reads and parses JSON from STDIN
        - generate_curl_command(): Creates formatted curl command with AWS headers

Supported AWS Headers:
    - x-amz-meta-filename
    - x-amz-meta-organizationid
    - x-amz-meta-correlationid
    - x-amz-meta-functionid
    - x-amz-tagging

Example Usage:
    echo '{
        "url": "https://example.com",
        "headers": {
            "x-amz-meta-filename": "test.zip",
            "x-amz-meta-organizationid": "org123",
            "x-amz-meta-correlationid": "corr123",
            "x-amz-meta-functionid": "func123",
            "x-amz-tagging": "tag1"
        }
    }' | python generate_curl_command.py

Error Handling:
    - Includes JSON parsing error handling
    - Logs error details for debugging
    - Exits with status code 1 on error
"""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JsonParser:
    def parse_json_from_stdin(self) -> Optional[Any]:
        """
        Read JSON data from STDIN and parse it into a Python structure
        Returns the parsed data or None if parsing fails
        """
        try:
            # Read all input from STDIN
            json_str = sys.stdin.read().strip()
            
            if not json_str:
                logger.error("No input received from STDIN")
                return None
                
            # Parse JSON into Python structure
            data = json.loads(json_str)
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            logger.error(f"Error at line {e.lineno}, column {e.colno}: {e.msg}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def generate_curl_command(self, data: Any) -> bool:
        """
        Print the parsed data structure
        Returns True if successful, False otherwise
        """

        output = f"""
        curl --request PUT '{data["url"]}' \
            --header 'x-amz-meta-filename: {data["headers"]["x-amz-meta-filename"]}' \
            --header 'x-amz-meta-organizationid: {data["headers"]["x-amz-meta-organizationid"]}' \
            --header 'x-amz-tagging: {data["headers"]["x-amz-tagging"]}' \
            --header 'x-amz-meta-correlationid: {data["headers"]["x-amz-meta-correlationid"]}' \
            --header 'x-amz-meta-functionid:  {data["headers"]["x-amz-meta-functionid"]}' \
            --header 'Content-Type: application/zip' \
            --data-binary '@/Users/john.carnell/work/gc-functions/cli/function-customer-example-nodejs.zip'
        """
        print(output)

def main():
    # Create parser instance
    json_parser = JsonParser()

    # Parse the JSON
    data = json_parser.parse_json_from_stdin()
    
    if data is None:
        sys.exit(1)
        
    # Print the parsed structure
    json_parser.generate_curl_command(data)
   
if __name__ == "__main__":
    main()

# >> END generate-curl-command-py