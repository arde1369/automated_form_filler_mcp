# Word Form MCP Server
### JM General Property & Liability Application — Voice/Text Intake + Auto-Fill

A Python MCP server for Claude Desktop that automates three things:
1. **Filling the JM Commercial Application form** via a voice/text interview
2. **Saving the completed document** to a folder on your computer
3. **Emailing the form** to a list of recipients via Office 365

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

You also need **LibreOffice** installed for `.doc` → `.docx` conversion:
- **macOS:** `brew install --cask libreoffice`
- **Windows:** Download from https://www.libreoffice.org/download

### 2. Set environment variables

```bash
export O365_EMAIL="you@yourcompany.com"
export O365_PASSWORD="your-app-password"
```

> If your Office 365 account has MFA enabled, generate an **App Password** at
> https://account.microsoft.com/security → Advanced security → App passwords.

### 3. Register with Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

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

Restart Claude Desktop after saving.

---

## How It Works — Full Example

Below is an exact example of how a broker would interact with Claude Desktop
using voice or text to fill out the **JM General Property & Liability Application**.

---

### Step 1 — Start the intake

**You say:**
> "Hey Claude, I need to fill out a JM Commercial Application form for a new client."

**Claude responds:**
> "Sure! I'll walk you through the JM General Property & Liability Application.
> Let's start with the broker info — what is your branch office name and producer name?"

---

### Step 2 — Broker Information

**You say:**
> "Branch office is North Vancouver. Producer is Roham Khoshgoo."

**Claude responds:**
> "Got it. What's today's date and the quote required by date?"

**You say:**
> "Date is May 1st 2026. Quote required by May 15th. Target premium is around $8,500."

**Claude responds:**
> "Perfect. Now let's move on to the client information. What is the name of the insured?"

---

### Step 3 — Client Information

**You say:**
> "The insured is Maple Ridge Construction Ltd."

**Claude responds:**
> "And their location address, city, province, and postal code?"

**You say:**
> "1240 Industrial Way, Maple Ridge, BC, V2X 4R3."

**Claude responds:**
> "Who is the contact person, and what's the best phone number and email?"

**You say:**
> "Contact is James Harrington, phone is 604-555-0182, cell is 604-555-0193,
> email is james@mapleridgeconstruction.ca."

**Claude responds:**
> "Do they have a website? And what is the mailing address — is it the same as the location?"

**You say:**
> "Website is mapleridgeconstruction.ca. Mailing address is the same."

**Claude responds:**
> "How many years have they been in business, and who are the principals?"

**You say:**
> "12 years in business. Principals are James Harrington and Linda Harrington."

**Claude responds:**
> "Can you give me a brief description of their business operations?"

**You say:**
> "They do general commercial construction — primarily tenant improvements and
> light industrial builds in the Lower Mainland."

---

### Step 4 — Current Policy Information

**Claude responds:**
> "Thanks. Now for their current policy — who is their current insurance company
> and when does the policy expire?"

**You say:**
> "They're with Intact. Expiry is August 1st 2026."

**Claude responds:**
> "Has their prior coverage been on a claims-made basis? And have they ever been
> cancelled for non-payment?"

**You say:**
> "No to both."

---

### Step 5 — Property Underwriting

**Claude responds:**
> "Now for the property details. How many storeys is the building, and what is
> the exterior wall construction?"

**You say:**
> "Two storeys, concrete block exterior."

**Claude responds:**
> "What year was it built, and what is the total area of the facility and the full building?"

**You say:**
> "Built in 1998. The facility is 6,200 square feet, the full building is 8,000 square feet."

**Claude responds:**
> "What type of roof construction, and is there a basement?"

**You say:**
> "Flat roof with modified bitumen membrane. No basement."

**Claude responds:**
> "What is the type of heat, and how would you rate the condition of the risk?"

**You say:**
> "Gas forced air. Condition is Good."

**Claude responds:**
> "Is the building sprinklered? And what are the wiring and plumbing types?"

**You say:**
> "Fully sprinklered — 100%. Wiring is copper with circuit breakers. Plumbing is copper."

---

### Step 6 — Liability Underwriting

**Claude responds:**
> "Moving on to liability. What are the estimated gross receipts, and do they
> have any operations or activities in the USA?"

**You say:**
> "Estimated gross receipts are $3.2 million. No US operations."

**Claude responds:**
> "How many full-time and part-time employees, and what is the total estimated payroll?"

**You say:**
> "18 full-time, 4 part-time. Total payroll around $1.4 million."

---

### Step 7 — Coverages Required

**Claude responds:**
> "Almost done — what liability limits are they looking for? Occurrence and aggregate?"

**You say:**
> "Two million occurrence, two million aggregate."

**Claude responds:**
> "Do they need building coverage? If so, what's the replacement cost value?"

**You say:**
> "Yes — building is $2.8 million replacement cost. Stock value is $150,000,
> equipment is $320,000."

**Claude responds:**
> "Great — I have everything I need. Here's a summary of what I've collected:"

```
Branch Office:             North Vancouver
Producer Name:             Roham Khoshgoo
Date:                      May 1, 2026
Quote Required By:         May 15, 2026
Target Premium:            $8,500
Name of Insured:           Maple Ridge Construction Ltd.
Location Address:          1240 Industrial Way
City:                      Maple Ridge
Province:                  BC
Postal Code:               V2X 4R3
Contact Person:            James Harrington
Phone Number:              604-555-0182
Cell Number:               604-555-0193
Email:                     james@mapleridgeconstruction.ca
Website:                   mapleridgeconstruction.ca
Years in Business:         12
Name of Principals:        James Harrington, Linda Harrington
Description of Operations: General commercial construction, tenant improvements
                           and light industrial builds, Lower Mainland
Current Insurance Company: Intact
Expiry Date:               August 1, 2026
Claims Made Basis:         No
Cancelled Non-Payment:     No
Height (Storeys):          2
Exterior Wall:             Concrete Block
Year Built:                1998
Total Area (Facility):     6,200 sq ft
Total Area (Building):     8,000 sq ft
Roof Construction:         Flat / Modified Bitumen
Basement:                  No
Type of Heat:              Gas Forced Air
Condition of Risk:         Good
Sprinklered:               Yes – 100%
Wiring Type:               Copper / Circuit Breakers
Plumbing Type:             Copper
Estimated Gross Receipts:  $3,200,000
US Operations:             No
Full-Time Employees:       18
Part-Time Employees:       4
Total Estimated Payroll:   $1,400,000
Liability Occurrence:      $2,000,000
Liability Aggregate:       $2,000,000
Building Value:            $2,800,000
Stock Value:               $150,000
Equipment Value:           $320,000
```

> "Shall I fill in the form, save it, and email it?"

---

### Step 8 — Fill, Save & Email

**You say:**
> "Yes — save it to my Documents/Applications folder and email it to
> underwriting@jminsurance.ca and my manager at sarah@ourbroker.com."

**Claude uses the MCP tools in sequence:**

1. `modify_word_form` — fills all fields into `template.doc` and saves a working copy
2. `save_document` — copies the completed form to `~/Documents/Applications/MapleRidgeConstruction_2026.docx`
3. `send_email` — sends the file to both recipients via Office 365

**Claude responds:**
> "Done! The completed JM Application for Maple Ridge Construction Ltd. has been
> saved to your Documents/Applications folder and emailed to underwriting@jminsurance.ca
> and sarah@ourbroker.com."

---

## Tool Reference

### `modify_word_form`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_path` | string | ✅ | Path to the `.doc` or `.docx` template |
| `output_path` | string | ✅ | Where to save the filled document |
| `fields` | object | ✅ | Label-to-value pairs matching form field labels |

### `save_document`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_path` | string | ✅ | Path to the filled document |
| `destination_folder` | string | ✅ | Target folder path |
| `new_filename` | string | ❌ | Rename the file (include `.docx`) |
| `move` | boolean | ❌ | Move instead of copy (default: false) |

### `send_email`
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recipients` | array | ✅ | List of TO addresses |
| `subject` | string | ✅ | Email subject |
| `body` | string | ✅ | Email body (plain text or HTML) |
| `attachment_path` | string | ❌ | Path to the completed form to attach |
| `cc` | array | ❌ | CC addresses |
| `is_html` | boolean | ❌ | True if body is HTML |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `SMTP authentication failed` | Use an App Password, not your regular password |
| `Template not found` | Use absolute paths in all tool calls |
| Field not filled in the document | Check that the label in `fields` matches the form label exactly |
| `.doc` conversion fails | Ensure LibreOffice is installed and `soffice` is in your PATH |
| MCP server not showing in Claude | Check `claude_desktop_config.json` syntax and restart Claude Desktop |
