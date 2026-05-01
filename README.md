# Word Form MCP Server

A Python MCP server for Claude Desktop that automates:
1. **Filling Word form templates** — replaces `{{PLACEHOLDER}}` fields in `.docx` files
2. **Saving documents** — copies/moves files to a target folder on disk
3. **Sending via Outlook** — emails the document to a list of recipients via Office 365 SMTP

---

## Setup

### 1. Install dependencies

```bash
cd word-form-mcp
pip install -r requirements.txt
```

### 1.a Run the installer (recommended)

You can run the installer script to complete setup automatically:

```bash
python install_mcp.py
```

What it does:
- Checks that `claude_desktop_config.json` exists in the default OS location
- Prompts for `O365_EMAIL` and `O365_PASSWORD`
- Creates a local `.env` file in this project
- Adds/updates the `word-form-mcp` entry in Claude Desktop config

If installation succeeds, it prints a success message. If it fails, it prints
the reason and what to fix.

### 2. Set environment variables

Add these to your shell profile (`~/.zshrc`, `~/.bashrc`, or system environment):

```bash
export O365_EMAIL="you@yourcompany.com"
export O365_PASSWORD="your-app-password"
```

> **MFA / Modern Auth:** If your Office 365 account has MFA enabled, generate an
> **App Password** at https://account.microsoft.com/security → Advanced security →
> App passwords. Use that as `O365_PASSWORD`.

### 3. Register with Claude Desktop

Add the following to your `claude_desktop_config.json`
(found at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS
or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "word-form-mcp": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/word-form-mcp/server.py"],
      "env": {
        "O365_EMAIL": "you@yourcompany.com",
        "O365_PASSWORD": "your-app-password"
      }
    }
  }
}
```

Replace `/ABSOLUTE/PATH/TO/word-form-mcp/` with the real path on your machine.

Restart Claude Desktop after saving.

---

## Word Template Format

In your `.docx` template, use double-brace placeholders:

```
Dear {{RECIPIENT_NAME}},

Please find the report for {{REPORT_DATE}} attached.

Regards,
{{SENDER_NAME}}
```

Placeholders work in:
- Body paragraphs
- Table cells
- Headers and footers

---

## Example Claude Prompts

**Fill and email a form:**
```
Fill in the contract template at /Users/me/templates/contract.docx with:
  - CLIENT_NAME: Acme Corp
  - DATE: April 24, 2026
  - AMOUNT: $15,000

Save it to /Users/me/documents/contracts/ as acme_contract.docx,
then email it to alice@acme.com and bob@acme.com with subject "Contract for Review".
```

**Batch workflow:**
```
Fill the invoice template with ORDER_ID=1042, CLIENT=TechCorp, TOTAL=$3,200.
Save to ~/invoices/ and email to billing@techcorp.com.
```

---

## Tool Reference

### `modify_word_form`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_path` | string | ✅ | Path to `.docx` template |
| `output_path` | string | ✅ | Where to save the filled document |
| `fields` | object | ✅ | `{"PLACEHOLDER": "value"}` pairs |

### `save_document`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_path` | string | ✅ | Path to source file |
| `destination_folder` | string | ✅ | Target folder path |
| `new_filename` | string | ❌ | Rename the file (include `.docx`) |
| `move` | boolean | ❌ | Move instead of copy (default: false) |

### `send_email`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recipients` | array | ✅ | List of TO addresses |
| `subject` | string | ✅ | Email subject |
| `body` | string | ✅ | Email body (text or HTML) |
| `attachment_path` | string | ❌ | File to attach |
| `cc` | array | ❌ | CC addresses |
| `is_html` | boolean | ❌ | True if body is HTML |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `SMTP authentication failed` | Use an App Password, not your regular password |
| `Template not found` | Use absolute paths in all tool calls |
| Placeholder not replaced | Ensure format is exactly `{{KEY}}` — no spaces inside braces |
| MCP server not showing in Claude | Check `claude_desktop_config.json` syntax and restart Claude |
