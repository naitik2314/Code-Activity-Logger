from main import summarize_changes

diff_text = """
- Removed deprecated API calls
+ Added logging to improve debugging
"""

summary = summarize_changes(diff_text)
print("Gemini Summary:", summary)

