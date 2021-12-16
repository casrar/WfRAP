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
  License: mit 
  Version: 1.0.0

    TODO:
        !!! BECOME REDDIT API COMPLIANT 
        !!Define several functions, general search, title search, content search(body and comments), username search are the core 
        !!Make into a class, more maintainable, can define var in constructor 
        !! make class structure make more sense, add in Oauth and such 
        !Work out functionality 
        !ADD IN TRY CATCHES, moreso just error handling
        !figure out how many entities it returns 
        !standardize naming conventions, and functions, make it make more sense 
    ERROR:
        Make search all comments more robust, breaks on certain pages
    THOUGHTS:
        More maintainable? or faster? 
        Create another methodto traverse posts, DRY, title and body repeat same code
        Im not sure why the amount of posts it returns is variable, kinda confusing

"""


import requests

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

    def _request_permalink(self, request: requests, i: int) -> requests:
        return request['data']['children'][i]['data']['permalink']

    # Searches all entites on a specific subreddit at a specific page, basis of all other search functions 
    def _search_request(self, subreddit: str, listing: str) -> requests:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/.json?after={listing}&limit=100' # default max limit is 100
            request = requests.get(url, headers = {'User-agent': self.user_agent}) # Need to read docs see what user-agent should be 
            return request.json()
        except:
            print('An Error Occured')
            return request.json()
    
    # Returns list of all titles in a subreddit, up to ()
    def search_all_titles(self, subreddit: str) -> list:
        title_list = []
        request = self._search_request(subreddit=subreddit, listing='')
        while True:
            num_dist = self._request_dist(request=request)
            for i in range(num_dist):
                title_list.append(self._request_title(request=request, i=i))

            new_listing = self._request_after(request=request)
            if (str(new_listing) == 'None'):
                return title_list

            request = self._search_request(subreddit=subreddit, listing=new_listing)

    # Returns list of all url in a subreddit, up to ()
    def _get_all_links(self, subreddit: str) -> list:
        permalink_list = []
        request = self._search_request(subreddit=subreddit, listing='')
        while True:
            num_dist = self._request_dist(request=request)
            for i in range(num_dist):
                permalink_list.append(self._request_permalink(request=request, i=i))

            new_listing = self._request_after(request=request)
            if (str(new_listing) == 'None'):
                return permalink_list

            request = self._search_request(subreddit=subreddit, listing=new_listing)

    # Returns list of all post bodies in a subreddit, up to () 
    def search_all_post_body(self, subreddit: str) -> list: 
        body_list = []
        request = self._search_request(subreddit=subreddit, listing='')
        count = 0
        while True:
            num_dist = self._request_dist(request=request)
            for i in range(num_dist):
                body_list.append(self._request_body(request=request, i=i))

            new_listing = self._request_after(request=request)
            if (str(new_listing) == 'None'):
                return body_list

            request = self._search_request(subreddit=subreddit, listing=new_listing)

    # Returns list of all comments in subreddit, up to ()
    # TODO - Abstract some of the searching and clean up the functions, a lot of patchwork going on
    # TODO - breaks if wikipage is present, account for other types of pages
    def search_all_comments(self, subreddit: str) -> list:
        permalink_list = self._get_all_links(subreddit=subreddit)
        comments = []
        for permalink in permalink_list:
            permalink = 'https://www.reddit.com' + permalink + '.json' # turn into a function, maybe
            request = requests.get(permalink, headers={'User-agent' : 'test'}).json()
            self._search_all_comments(request[1]['data']['children'], comments) # turn into a function
        
        return comments

    # Function that parses post and returns all comments // May be missing certain functionality 
    def _search_all_comments(self, request: requests, comments: list) -> None:
        for i in range(len(request)):
            if request[i]['kind'] == 'more': # skip if not comment/reply
                continue

            comment = request[i]['data']['replies'] # turn into a function
            if comment == "":
                comment_body = request[i]['data']['body'] # turn into a function
                comments.append(comment_body)
            else:
                children = comment['data']['children'] # turn into a function
                self._search_all_comments(children, comments)
                comment_body = request[i]['data']['body'] # turn into a function
                comments.append(comment_body)
    
    # for internal testing, remove when finished
    def _test(self) -> None:
        pass
       



