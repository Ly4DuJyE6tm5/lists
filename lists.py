import requests
from datetime import datetime

ignored_words = ["list_of_domains_to_ignore.tld"]  # List of words to ignore


def download_file(url, filename):
    """Downloads a file from the specified URL and saves it as the given filename,
    filtering out lines that don't start with "0.0.0.0".

    Args:
      url: The URL of the file to download.
      filename: The filename to save the file as.
    """
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "w") as f:
            for line in response.text.splitlines():
                if line.startswith("0.0.0.0") and all(
                    word not in line.lower() for word in ignored_words
                ):  # Check for all ignored words (case-insensitive)
                    f.write(line + "\n")
        print(f"File downloaded and filtered successfully: {filename}")
    else:
        print(f"Failed to download file: {url}")


def merge_and_deduplicate(filenames, output_filename):
    """Merges content from multiple files, sorts, removes duplicates, and saves to a new file,
    filtering out lines that don't start with "0.0.0.0".

    Args:
      filenames: A list of filenames to merge.
      output_filename: The filename to save the merged and deduplicated content.
    """
    merged_content = []
    for filename in filenames:
        try:
            with open(filename, "r") as f:
                merged_content.extend(
                    line.strip() for line in f if line.startswith("0.0.0.0")
                )  # Filter and remove trailing whitespaces
        except FileNotFoundError:
            print(f"File not found: {filename}")

    # Sort the merged content
    merged_content.sort()

    # Remove duplicates while keeping the order
    unique_content = []
    seen = set()
    for line in merged_content:
        if line not in seen:
            unique_content.append(line)
            seen.add(line)

    # Get current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write content with comment
    with open(output_filename, "w") as f:
        f.write(
            f"# This file was generated on {now} and contains {len(unique_content)} lines.\n\n"
        )
        f.writelines(content + "\n" for content in unique_content)
    print(f"Merged, sorted, and deduplicated content saved to: {output_filename}")


# Download files (filtering during download)
download_file(
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/samsung",
    "samsung_domains.txt",
)
download_file(
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/windows",
    "windows_domains.txt",
)
download_file(
    "https://www.github.developerdan.com/hosts/lists/facebook-extended.txt",
    "facebook-extended.txt",
)
download_file(
    "https://blocklistproject.github.io/Lists/everything.txt", "blocklistproject.txt"
)
download_file(
    "https://github.com/blocklistproject/Lists/blob/master/whatsapp.txt", "whatsapp.txt"
)
download_file("https://adaway.org/hosts.txt", "adaway.txt")
download_file("https://v.firebog.net/hosts/AdguardDNS.txt", "adguarddns.txt")


# Merge, sort, and deduplicate (filtering during merge)
merge_and_deduplicate(
    ["samsung_domains.txt", "windows_domains.txt", "facebook-extended.txt"],
    "merged_blocklist.txt",
)
