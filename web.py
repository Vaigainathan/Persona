import requests
import google.generativeai as genai

# === Configuration ===
SERP_API_KEY = "dda365093a67b3e48319c8f9ef3e6e544ac962ec8a8e7325de41a52ca2a8acfe"
GENAI_API_KEY = "AIzaSyA_-GNZghO3OOA_h1pcN15kxVnRajomY9s"

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(model_name="gemma-3-27b-it")

# === Step 1: Search Google and LinkedIn ===
def google_search(query, num_results=5):
    search_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": num_results
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    extracted_info = []
    for res in results.get("organic_results", []):
        title = res.get("title")
        snippet = res.get("snippet")
        link = res.get("link")
        if title and snippet:
            extracted_info.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
        if len(extracted_info) >= num_results:
            break
    return extracted_info

# === Step 2: LinkedIn Specific Search ===
def linkedin_search(name):
    query = f"{name} site:linkedin.com"
    results = google_search(query, num_results=1)
    return results[0] if results else None

# === Step 3: Prepare Prompt ===
def generate_prompt(info_blocks, name, organization, org_type):
    combined_text = "\n\n".join(info_blocks)
    return (
        f"Summarize the following details into a professional and personal profile of {name}, "
        f"who is associated with {organization}, which is a {org_type} organization.\n\n{combined_text}"
    )

# === Step 4: Summarize with Gemini ===
def summarize_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Summarization error: {str(e)}"

# === Step 5: Full Pipeline ===
def get_person_summary(name, organization, org_type):
    print(f"Searching for: {name} {organization} {org_type}\n")

    # General Google Search
    general_info = google_search(f"{name} {organization} {org_type}")

    # LinkedIn Search
    linkedin_info = linkedin_search(name)
    if linkedin_info:
        print("\nLinkedIn Profile Found!\n")
    else:
        print("\nNo LinkedIn Profile found.\n")

    info_blocks = []

    if linkedin_info:
        info_blocks.append(linkedin_info)

    info_blocks.extend(general_info)

    if not info_blocks:
        return "No useful search results found."

    print("\nGenerating Summary...\n")
    prompt = generate_prompt(info_blocks, name, organization, org_type)
    summary = summarize_with_gemini(prompt)
    return summary

# === Example Usage ===
if __name__ == "__main__":
    name = input("Enter person name: ")
    organization = input("Enter organization name: ")
    org_type = input("Enter type of organization (e.g., politics, Bollywood, tech): ")
    result = get_person_summary(name, organization, org_type)
    print("\n--- SUMMARY ---\n")
    print(result)