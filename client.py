import requests
import sys
import os

# Bypass proxy
os.environ["NO_PROXY"] = "127.0.0.1"


def upload_file_to_cpg_server(file_path: str, server_url: str = "http://127.0.0.1:8000"):
    """
    Upload a file to the CPG server and print the JSON response.
    """

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "text/plain")}

        print(f"Uploading {file_path} to {server_url}/cpg...")
        response = requests.post(f"{server_url}/cpg", files=files)


    if response.status_code == 200:
        print("✅ Success! CPG analysis result:")
    else:
        print(f"❌ Error: Server returned status code {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <file_to_analyze>")
        sys.exit(1)

    file_path = sys.argv[1]
    upload_file_to_cpg_server(file_path)
