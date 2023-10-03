import requests

# Define the base URL for the GitHub API's pull requests endpoint.
BASE_URL = "https://api.github.com/repos/{owner}/{repo}/pulls"

def get_repo_info(owner, repo):
    url = BASE_URL.format(owner=owner, repo=repo)
    response = requests.get(url, params={'state': 'open', 'per_page': 1}) # request only 1 item to minimise data transfer and mainly check for pagination.

    if response.status_code != 200:
        print(f"Error: Unable to fetch data from {owner}/{repo}. Error Code is {response.status_code}")
        return None

    #Check if the link is in the header. If it doesn't exist, it means all results are on the first page
    if 'link' in response.headers:
        links = response.headers['link'].split(',')
        for link in links:
            if 'rel="last"' in link:
                last_url = link.split(';')[0].strip('>')
                last_page_num = last_url.split('=')[-1]
                return last_page_num
        
    return len(response.json())
    

def main():
    print("Welcome to Multitudes CLI! Let’s process some Github Data!")
    owner = input("Who is the repo owner? ")
    repo = input("What is the repo name?")
    print(f"Excellent! Querying {owner}/{repo} for open PRs!")

    count = get_repo_info(owner, repo)
    if count != 0:
        print(f"# of open PRs: {count}")
    print("Bye")


if __name__ == "__main__":
    main()





    
