"""
\\          //     ////      ////      //// 
 \\  //\\  //     ||__//   ||___//   ||___//    
  \\//  \\//   f  ||  \\   ||   //   ||    

  A simple wrapper for the Reddit API. Part project to learn about APIs also
  partly useful so I can use it in other projects to make my life sweet as pie.
  Also, gonna try my hardest to make the API easy to use for idiots such as myself.
  I need something to work on and help me learn Python and its conventions,
  also I can add to my Git >:).

  Author: Casey Morar (casrar)
  License: no clue
  Version: 0.1

    TODO:
        Define several functions 
        Work out functionality 
    ERROR:

"""


import requests
from requests.api import request

# Function that needs to be fleshed out, wanna work on some flags and functionality 
# As of rn this may be my most low level function, can probably leverage it for othe functions i have planned
# idk
def search_all_request(subreddit: str, listing: str, pages: int) -> requests:
    try:
        url = f'https://www.reddit.com/r/{subreddit}/.json?after={listing}&limit=100'
        request = requests.get(url, headers = {'User-agent': 's'}) # I'm truly not sure what user agent header does, GB google ig
        print(request.status_code)
        request = request.json()
        return request
    except:
        print('An Error Occured')
        return request.json()
  

r = search_all_request(subreddit = 'API', listing = '', pages = 100)
new_listing = ''
while True:
    num_dist = r['data']['dist']
    for i in range (num_dist):
        print(r['data']['children'][i]['data']['title'])
    # print('\n\n\n')
    # print(new_listing) Testing stuff i didnt remove yet 
    # print('\n\n\n')

    new_listing = r['data']['after']
    if (str(new_listing) == 'None'):
        break

    r = search_all_request(subreddit = 'API', listing = new_listing, pages = 100)


