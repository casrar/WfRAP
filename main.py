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
    THOUGHTS:
        More maintainable? or faster? 
        Create another methodto traverse posts, DRY, title and body repeat same code
        Base functionality is complete, MVP achieved, now is just figuring out comments
        

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
        while True:
            num_dist = self._request_dist(request=request)
            # print(num_dist)
            body_list.append([self._request_body(request=request, i=i) for i in range(num_dist)])
            # print(title_list)
            new_listing = self._request_after(request=request)
            # print(new_listing)
            if (str(new_listing) == 'None'):
                return body_list
            request = self._search_request(subreddit=subreddit, listing=new_listing)

    # Currently deprecated until I can figure out wtf to do
    def search_all_comments(self) -> None:
        pass

  



s = Search('test')
test = s.search_all_post_body('Python')
print(test)


    # JESUS CHRIST COMMENTS ARE GONNA MAKE ME CRY
    # def search_all_comments(self, subreddit: str, user_agent: str) -> list:
    #     request = requests.get('https://www.reddit.com/r/linux_gaming/comments/rdfv7i/obs_studio_and_fedora_linux_an_interview_with/.json', headers = {'User-agent': user_agent})
    #     request = request.json()
    #     if request[1]['data']['children'] == []:
    #         print('No Comments')

        # print(request[1]['data']['children'][0]['data']['replies']['data']['children'][0]['data']['replies']['data']['children'][0]['data']['body'])
        # from search request, the children permalink offers a link to the subreddit from which you can grab the comments
        # essentially I grab 1->data->children-># and dig deeper into data and replies
        # some info, page response 0 is the post
        # the O runtime of this is going to legitimately be so awful
        # might actually warrant me writing something in C if im not lazy
        # loop over all posts on reddit, with a loop over every post for all comments, with a loop to enter each comment thread
        # I may even be missing one, at the fastest it has to be O(n^3) unless im missing something 
        # more like n^7 LOL
        # 
        # Only solution ive come up with tha kinda makes sense, KINDA, dont know if its even possible
        # enterTraverse(input)
        # if [1][data][children] if != []
        #     return
        # else traverse(input)

        # traverse(input)
        # for childern in children:
        #     if replies == ""
        #         list.append(body)
        #     else
        #         traverse([data][replies][data][children])

