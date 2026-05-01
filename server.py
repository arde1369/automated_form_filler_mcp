"""
Word Form MCP Server
Provides tools to modify Word forms, save documents, and send via Outlook.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

from tools.word_tool import modify_word_form
from tools.file_tool import save_document
from tools.email_tool import send_email

app = Server("word-form-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="modify_word_form",
            description=(
                "Fill in placeholders or form fields in a Word (.docx) template. "
                "Placeholders should be in the format {{FIELD_NAME}} in the template. "
                "Returns the path to the modified document."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "template_path": {
                        "type": "string",
                        "description": "Absolute path to the Word (.docx) template file."
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Absolute path where the filled document will be saved."
                    },
                    "fields": {
                        "type": "object",
                        "description": (
                            "Key-value pairs where keys match placeholder names in the template "
                            "(e.g. {\"NAME\": \"John Smith\", \"DATE\": \"2026-04-24\"}). "
                            "Placeholders in the doc should be {{KEY}}."
                        ),
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["template_path", "output_path", "fields"]
            }
        ),
        Tool(
            name="save_document",
            description=(
                "Copy or move a document file to a specified destination folder on disk. "
                "Returns the final saved path."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "Absolute path to the source document."
                    },
                    "destination_folder": {
                        "type": "string",
                        "description": "Absolute path to the destination folder."
                    },
                    "new_filename": {
                        "type": "string",
                        "description": "Optional new filename (including .docx extension). If omitted, the original filename is used."
                    },
                    "move": {
                        "type": "boolean",
                        "description": "If true, move the file instead of copying. Default: false (copy)."
                    }
                },
                "required": ["source_path", "destination_folder"]
            }
        ),
        Tool(
            name="send_email",
            description=(
                "Send an email with an optional document attachment via Outlook / Office 365. "
                "Supports multiple recipients. Uses SMTP with Office 365."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recipient email addresses."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line."
                    },
                    "body": {
                        "type": "string",
                        "description": "Plain text or HTML body of the email."
                    },
                    "attachment_path": {
                        "type": "string",
                        "description": "Optional absolute path to a file to attach."
                    },
                    "cc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of CC email addresses."
                    },
                    "is_html": {
                        "type": "boolean",
                        "description": "Set to true if the body contains HTML. Default: false."
                    }
                },
                "required": ["recipients", "subject", "body"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "modify_word_form":
            result = modify_word_form(
                template_path=arguments["template_path"],
                output_path=arguments["output_path"],
                fields=arguments["fields"]
            )
        elif name == "save_document":
            result = save_document(
                source_path=arguments["source_path"],
                destination_folder=arguments["destination_folder"],
                new_filename=arguments.get("new_filename"),
                move=arguments.get("move", False)
            )
        elif name == "send_email":
            result = send_email(
                recipients=arguments["recipients"],
                subject=arguments["subject"],
                body=arguments["body"],
                attachment_path=arguments.get("attachment_path"),
                cc=arguments.get("cc", []),
                is_html=arguments.get("is_html", False)
            )
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
