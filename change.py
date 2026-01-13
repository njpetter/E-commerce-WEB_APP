import os
import json

# Configuration
LOCAL_URL = "http://localhost:8000"
TARGET_DIR = os.path.join(os.getcwd(), "client", "src")
ROOT_PACKAGE_JSON = os.path.join(os.getcwd(), "package.json")

def implement_final_changes():
    # --- Part 1: Update root package.json for Railway Build ---
    print("Updating root package.json build scripts...")
    if os.path.exists(ROOT_PACKAGE_JSON):
        try:
            with open(ROOT_PACKAGE_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Ensure scripts dictionary exists
            if "scripts" not in data:
                data["scripts"] = {}
                
            # This is the crucial command for Railway deployment
            data["scripts"]["build"] = "npm install && cd client && npm install && npm run build"
            
            with open(ROOT_PACKAGE_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("SUCCESS: root package.json updated with build script.")
        except Exception as e:
            print(f"ERROR updating package.json: {e}")
    else:
        print("ERROR: Could not find root package.json. Are you in the right folder?")

    # --- Part 2: Convert Localhost to Relative Paths ---
    print(f"\nConverting URLs to Relative Paths in: {TARGET_DIR}")
    count = 0
    if not os.path.exists(TARGET_DIR):
        print(f"ERROR: Target directory {TARGET_DIR} does not exist.")
        return

    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith((".jsx", ".js")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if LOCAL_URL in content:
                        # Strips the domain so it calls the same host it's served from
                        new_content = content.replace(LOCAL_URL, "")
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"SUCCESS: Updated {file}")
                        count += 1
                except Exception as e:
                    # Using ascii to avoid further print errors
                    print(f"WARNING: Skipping {file} due to error.")

    if count > 0:
        print(f"\nSuccessfully updated {count} frontend files.")
    else:
        print("\nNo localhost URLs found. They may have been updated already!")

    print("\n--- PROCESS COMPLETE ---")
    print("Next steps:")
    print("1. Commit these changes and push to GitHub.")
    print("2. Railway will run the new 'build' script automatically.")
    print("3. Wait for the 'Building' status to finish (takes 2-5 mins).")

if __name__ == "__main__":
    implement_final_changes()