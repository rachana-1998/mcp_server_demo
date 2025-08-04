"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""
import os
import json
import re
from datetime import datetime



from presentation_manager import generate_slide

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")




# Add a ppt generation tool
@mcp.tool()
def generate_presentation(json_input: str, output_dir: str = "presentation") -> str:
    """
    Generate a PowerPoint presentation from a JSON string or JSON file.
    Saves the presentation as a .pptx in the specified output directory.
    """
    try:
        # Check if input is a path to a JSON file
        if os.path.isfile(json_input):
            with open(json_input, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            # Otherwise assume it's a JSON string
            data = json.loads(json_input)

        # Validate structure
        if not isinstance(data, dict) or "topic" not in data or "slides" not in data:
            return "Invalid JSON format. Must include 'topic' and 'slides'."

        # Extract and sanitize topic to build filename
        topic = data["topic"]
        topic = re.sub(r'[^\w\s-]', '', topic).strip().replace(" ", "_").lower()
        if not topic:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            topic = f"presentation_{timestamp}"

        # Create output directory and output file path

        current_dir=os.getcwd()
        final_output_dir=os.path.join(current_dir,output_dir)
        os.makedirs(final_output_dir, exist_ok=True)
        output_path = os.path.join(final_output_dir, f"{topic}.pptx")

        # Save JSON to a temp file
        temp_json_path = os.path.join(final_output_dir, f"{topic}_temp.json")

        print(temp_json_path)
        with open(temp_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Generate the slide deck from the temp JSON file
        generate_slide(temp_json_path, output_path)

        # Optionally delete the temp file
        os.remove(temp_json_path)

        return f"✅ Presentation successfully saved as: {output_path}"

    except json.JSONDecodeError:
        return "Failed to parse input as JSON. Make sure it's a valid JSON string or file."
    except Exception as e:
        return f"Error generating presentation: {str(e)}"

def generate_slide(json_file_path, output_pptx_path):
    """
    Dummy implementation: replace this with real slide generation logic.
    """
    print(f"Would generate slide deck from {json_file_path} to {output_pptx_path}")
    # Example: you could load json_file_path, and use python-pptx to build slides.


#
# # add a prompt for ppt generation
@mcp.prompt()
def presentation_prompt(topic: str, tone: str = "student") -> str:
    """
    Generate a prompt for creating a PowerPoint presentation on a given topic and tone.
    The prompt instructs the model to produce JSON only (no HTML or markdown).
    """
    tones = {
        "business": (
            "Create a formal and professional PowerPoint presentation for a business audience. "
            "Use concise bullet points, data visualizations, and structured formatting."
        ),
        "student": (
            "Create an educational and engaging PowerPoint presentation for students. "
            "Use clear explanations, visual aids, and simple language."
        ),
        "teacher": (
            "Create an instructional PowerPoint presentation for teachers. "
            "Include detailed concepts, examples, and talking points for classroom teaching."
        ),
        "child": (
            "Create a fun and colorful PowerPoint presentation for children. "
            "Use simple language, large fonts, and cartoon-style images."
        ),
    }

    instruction = tones.get(tone.lower(), tones["student"])

    return (
        f"{instruction}\n\n"
        f"Topic: \"{topic}\"\n\n"
        f"**Important:** Only output JSON — do NOT include any explanation, markdown, or HTML.\n\n"
        f"The JSON structure must look like this:\n"
        f"{{\n"
        f"  \"topic\": \"{topic}\",\n"
        f"  \"slides\": [\n"
        f"    {{\n"
        f"      \"slide_number\": 1,\n"
        f"      \"slide_type\": \"title\",\n"
        f"      \"title\": \"Slide Title\",\n"
        f"      \"subtitle\": \"Optional subtitle\",\n"
        f"      \"content\": {{\n"
        f"        \"main_text\": \"Main text or introduction\",\n"
        f"        \"bullet_points\": [\"Point 1\", \"Point 2\"],\n"
        f"        \"visual_elements\": [\"🌿\", \"📊\"]\n"
        f"      }}\n"
        f"    }},\n"
        f"    ... (additional slides)\n"
        f"  ]\n"
        f"}}"
    )



