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
        !!Define several functions, general search, title search, content search(body and comments), username search are the core 
        !!Make into a class, more maintainable, can define var in constructor 
        !Work out functionality 
        !ADD IN TRY CATCHES, moreso just error handling
        !!! GET COMMENTS WORKING
    ERROR:
        Cant get comment working, as of RN it is deprecated 
        Im not sure why the amount of posts it returns is variable, kinda confusing
    
    THOUGHTS:
        More maintainable? or faster? 
        Create another methodto traverse posts, DRY, title and body repeat same code
        Base functionality is complete, MVP achieved, now is just figuring out comments
        

"""


import requests
from typing import Union

class Search:

    def __init__(self, user_agent: str) -> None:
        self.user_agent = user_agent
        pass
    
    # Functions to perform repetitive request activites, using for DRY 
    def _request_title(self, request: requests, i: int) -> requests:
        return request['data']['children'][i]['data']['title']

    def _request_after(self, request: requests) -> requests:
        return request['data']['after']

    def _request_dist(self, request: requests) -> requests:
        return request['data']['dist']

    def _request_body(self, request: requests, i: int) -> requests:
        return request['data']['children'][i]['data']['selftext']

    # Searches all entites on a specific subreddit at a specific page, basis of all other search functions 
    def _search_request(self, subreddit: str, listing: str) -> requests:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/.json?after={listing}&limit=100' # default max limit is 100
            request = requests.get(url, headers = {'User-agent': self.user_agent}) # I'm truly not sure what user agent header does, GB google ig
            #print(request.status_code)
            #request = request.json()
            return request.json()
        except:
            print('An Error Occured')
            return request.json()
    
    # Returns list of all titles in a subreddit up to 1000 entities
    def search_all_titles(self, subreddit: str) -> list:
        title_list = []
        request = self._search_request(subreddit=subreddit, listing='')
        while True:
            num_dist = self._request_dist(request=request)
            # print(num_dist)
            # change back to for loop
            title_list.append([self._request_title(request=request, i=i) for i in range(num_dist)])
            # print(title_list)
            new_listing = self._request_after(request=request)
            # print(new_listing)
            if (str(new_listing) == 'None'):
                return title_list
            request = self._search_request(subreddit=subreddit, listing=new_listing)

    # Returns list of all post bodies in a subreddit, up to 1000 entries 
    def search_all_post_body(self, subreddit: str) -> list: 
        body_list = []
        request = self._search_request(subreddit=subreddit, listing='')
        count = 0
        while True:
            num_dist = self._request_dist(request=request)
            # print(num_dist)

            # changed back to traditional for loop, my list comprehension was nesting my loops
            for i in range(num_dist):
                body_list.append(self._request_body(request=request, i=i))
                count = count+1
            # Deprecated
            # body_list.append([self._request_body(request=request, i=i) for i in range(num_dist)])

            # print(title_list)
            new_listing = self._request_after(request=request)
            # print(new_listing)
            if (str(new_listing) == 'None'):
                print(count)
                return body_list
            request = self._search_request(subreddit=subreddit, listing=new_listing)

    def search_all_comments(self) -> None:
        url = 'https://www.reddit.com/r/linux_gaming/comments/reup3p/openrazer_32_released_for_supporting_more_razer/.json' 
        request = requests.get(url, headers = {'User-agent': 'a'})
        request = request.json()
        # print(len(request[0]['data']['children'][0]['data']['subreddit']))
        # print(request[0]['kind']['children'])
        
        # print(request[0]['data']['children'][0]['kind'])
        comments = []
        self._search_all_comments(request[1]['data']['children'], comments)
        return comments


    # Currently deprecated until I can figure out wtf to do
    # I figured out wtf to do, god bless recursion 
    def _search_all_comments(self, request: requests, comments: list): #-> requests & list:
        for i in range(len(request)):
            comment = request[i]['data']['replies'] # turn into a  function
            # print(str(name))
            if comment == "":
                comment_body = request[i]['data']['body']
                comments.append(comment_body)
            else:
                children = comment['data']['children']
                self._search_all_comments(children, comments)
                comment_body = request[i]['data']['body']
                comments.append(comment_body)
                
            #pass
        # iterate over reply[i][data]
        #for comments in request
            # if replies != ""
                # search (request['replies']['data']['children'])
            # else 
                # comments.append(request['body'])
    
    def test(self) -> None:
        # request = requests.get('https://www.reddit.com/r/linux_gaming/comments/reup3p/openrazer_32_released_for_supporting_more_razer/.json')
        # request = request.json()
        url = 'https://www.reddit.com/r/linux_gaming/comments/reup3p/openrazer_32_released_for_supporting_more_razer/.json' 
        request = requests.get(url, headers = {'User-agent': 'a'})
        request = request.json()
        test1 = request[0]['data']['children'][0]['data']['preview']
        print(test1)
        print('\n\n\n\n\n')
        test2 = test1['images'][0]['resolutions'][0]['url']
        print(test2)



