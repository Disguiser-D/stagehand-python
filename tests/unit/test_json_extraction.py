"""Tests for JSON extraction from mixed content."""

import pytest

from stagehand.utils import extract_json_from_mixed_content


class TestJsonExtraction:
    """Test cases for extracting JSON from mixed content responses."""

    def test_direct_json_parsing(self):
        """Test that direct JSON parsing still works for backward compatibility."""
        content = '{"elements": [{"element_id": 123, "description": "test"}]}'
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element_id"] == 123

    def test_json_code_block_extraction(self):
        """Test extraction from ```json code blocks."""
        content = """Looking at the accessibility tree, I can find the link for '行情' (Market/Quotes).
In the navigation area near the top of the page, there is a div containing 
navigation links, and one of them is:
```
[293] link: 行情
```
This link is located at element ID 293 in the accessibility tree, within the 
navigation section of the page header.
```json
[
  {
    "element": "link",
    "text": "行情",
    "id": 293
  }
]
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element"] == "link"
        assert result["elements"][0]["text"] == "行情"
        assert result["elements"][0]["id"] == 293

    def test_json_array_extraction_without_code_block(self):
        """Test extraction of JSON arrays not in code blocks."""
        content = """The element is available here:
[
  {
    "element_id": 456,
    "description": "A clickable button",
    "method": "click",
    "arguments": []
  }
]
Let me know if you need more details."""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element_id"] == 456

    def test_json_object_extraction(self):
        """Test extraction of standalone JSON objects."""
        content = """Here's the result: {"elements": [{"element_id": 789, "description": "test object"}]}"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element_id"] == 789

    def test_multiple_json_blocks_returns_first_valid(self):
        """Test that when multiple JSON blocks exist, the first valid one is returned."""
        content = """Here are multiple options:
```json
[
  {
    "element_id": 111,
    "description": "first option"
  }
]
```

And another option:
```json
[
  {
    "element_id": 222,
    "description": "second option"
  }
]
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element_id"] == 111
        assert result["elements"][0]["description"] == "first option"

    def test_malformed_json_fallback(self):
        """Test handling of malformed JSON."""
        content = """Some text with malformed JSON:
{
  "element_id": 123,
  "description": "missing closing brace"
"""
        
        result = extract_json_from_mixed_content(content)
        
        # Should return empty elements when no valid JSON is found
        assert result == {"elements": []}

    def test_empty_content(self):
        """Test handling of empty or None content."""
        assert extract_json_from_mixed_content("") == {"elements": []}
        assert extract_json_from_mixed_content(None) == {"elements": []}

    def test_no_json_content(self):
        """Test handling of content with no JSON."""
        content = "This is just plain text with no JSON content whatsoever."
        
        result = extract_json_from_mixed_content(content)
        assert result == {"elements": []}

    def test_complex_mixed_content_with_chinese_text(self):
        """Test the exact scenario from the user's example."""
        content = """Looking at the 
accessibility tree, I can find the link for '行情' (Market/Quotes).
In the navigation area near the top of the page, there is a div containing 
navigation links, and one of them is:
```
[293] link: 行情
```
This link is located at element ID 293 in the accessibility tree, within the 
navigation section of the page header.
```json
[
  {
    "element": "link",
    "text": "行情",
    "id": 293
  }
]
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        element = result["elements"][0]
        assert element["element"] == "link"
        assert element["text"] == "行情"
        assert element["id"] == 293

    def test_nested_json_objects(self):
        """Test extraction of nested JSON structures."""
        content = """Here's a complex element:
```json
{
  "elements": [
    {
      "element_id": 100,
      "description": "Complex element",
      "properties": {
        "visible": true,
        "clickable": false
      },
      "children": [
        {"id": 101, "type": "text"},
        {"id": 102, "type": "button"}
      ]
    }
  ]
}
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        element = result["elements"][0]
        assert element["element_id"] == 100
        assert "properties" in element
        assert element["properties"]["visible"] is True
        assert len(element["children"]) == 2

    def test_json_with_special_characters(self):
        """Test extraction of JSON containing special characters."""
        content = """Here's an element with special characters:
```json
[
  {
    "element_id": 200,
    "text": "Submit & Continue →",
    "description": "Button with symbols & unicode",
    "xpath": "//button[@class='btn-submit']"
  }
]
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        element = result["elements"][0]
        assert element["text"] == "Submit & Continue →"
        assert element["xpath"] == "//button[@class='btn-submit']"

    def test_case_insensitive_json_blocks(self):
        """Test that JSON block extraction is case insensitive."""
        content = """Here's the data:
```JSON
[
  {
    "element_id": 300,
    "description": "uppercase JSON block"
  }
]
```"""
        
        result = extract_json_from_mixed_content(content)
        
        assert "elements" in result
        assert len(result["elements"]) == 1
        assert result["elements"][0]["element_id"] == 300