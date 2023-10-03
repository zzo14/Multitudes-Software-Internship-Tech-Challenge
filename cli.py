import requests

# Cute ASCII Art
print("""
  /\_/\  
 ( o.o )
  > ^ <                               
""")

# Define the base URL for the GitHub API's pull requests endpoint.
BASE_URL = "https://api.github.com/repos/{owner}/{repo}/pulls"
RATE_LIMIT_URL = "https://api.github.com/rate_limit"

def check_rate_limit():
    response = requests.get(RATE_LIMIT_URL)
    remaining = response.json()["resources"]["core"]["remaining"]
    return remaining

def get_repo_info(owner, repo):
    # check the rate limit for the GitHub API.
    if check_rate_limit() == 0:
        print("Rate limit exceeded! Please wait before making more requests.")
        return None

    url = BASE_URL.format(owner=owner, repo=repo)
    response = requests.get(url, params={'state': 'open', 'per_page': 1}) # request only 1 item to minimise data transfer and mainly check for pagination.

    if response.status_code != 200:
        print(f"Error: Unable to fetch data from {owner}/{repo}. Error Code is {response.status_code}")
        return None
    
    # If there's no link header, return the count of the current page
    if 'link' not in response.headers:
        return len(response.json())

    #Check for pagination
    links = response.headers['link'].split(',')
    for link in links:
        if 'rel="last"' in link:
            last_url = link.split(';')[0].strip('>')
            last_page_num = last_url.split('=')[-1]
            return last_page_num

    

def main():
    print("Welcome to Multitudes CLI! Let’s process some Github Data!")
    owner = input("Who is the repo owner? ")
    repo = input("What is the repo name?")
    print(f"Excellent! Querying {owner}/{repo} for open PRs!")

    count = get_repo_info(owner, repo)
    if count is None:
        print("There was a problem querying the repo.")
    elif count == 0:
        print(f"There are no open pull requests for {owner}/{repo}.")
    else:
        print(f"# of open PRs: {count}")
    print("Bye")


if __name__ == "__main__":
    main()





    
