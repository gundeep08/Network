# Below is the description of Each File created

### index.html
 This template is the default file to be loaded on startup of application and displays all the post and its details like post content, creation time, postOwner that the current user is eligibile to access or see. If the user is signedIn, user can like or follow other users/posts as well. This page also ensures celebrity accounts has there account user name shown in golder color. Also the owner of the post will have an option of editing his post with the button on index page against that post.Non-owner of the post will have the option to repost that post by clicking on the repost link against that post in index.html.Pagination is also implemented to make sure no more than 10 post are shown on a single page.

 ### Profile.html
 This template is used to display all the post by the specific user whose profile has been requested, this template also provides the option of follow/unfollow that user and also give you a hyperlink to view the details of all the followers or follows of that user.

 ### AddPost.html
 This template is to add a new post and is only accessible for signedIn users, in this user can add content of the post and also set the scope of the post.

 ### Repost.html
 This Template is used for repost option, only the non-owner signedIn user can access that feature for a particular post, in this template user cannot change the content of the post but can change the visibility scope of the post.

 ### Edit.html
 This template is used for editing of your post and this template can be accessed only by the owner of the post and that too when he/she is signedIn. In this user can edit the post content and also change the visibility scope of that post.

 ### FollowerDetails.html
 This template displays all the user details like username, number of posts, number of followers, number of follows for all the followers of the selected users. Username is a hyperlink and will be redirected to profile page of that user.

 ### FollowingDetails.html
 This template displays all the user details like username, number of posts, number of followers, number of follows for all the follows of the selected users. Username is a hyperlink and will be redirected to profile page of that user.

 ### Search.html
 This template is used to search post from a particular user or/and based on a date range, this feature can be used by both SignedIn and SignedOut users, on click of search user is redirected to index page with filtered set of posts.

 ### Message.html
 This template is used to view messages to the current signedIn user, user can also send a message and view the sent messages, this feature is only for thesignedIn user and all the read messages will be greyed out. On message body user will have option to reply to a message and on sucessfull reply, user will be redirected to sent messages.

 ### network.js
 This Javascript file is used to make fetch calls for calculating likes on a particular post and followers and follows of a particular user, this js file is used by index.html, Profile.html template and following template.

### message.js
This Javascript file is used to make fetch calls to pull messages based on request and message.html uses this javascript file.

### template_name.py
This .py file is used to define the different filters for checking elements in a list or a filter to fetch the dictionary value based on a specific key.

### view.py
This will include the buisness logic for all the flows before routing it to its respective templates.

### urls.py
This will include all the routes, methods of view.py to be invoked on a particular url route is also configured there.

### Models.py
This will also include all the model objects like Posts, Likes, Follow, Message, Following and all the fields for its class.


# Major Accomplishments with Sub-details.

## Add Scope to each Post:
### SubDetails:
	• While creating a Post, user would be given option to restrict the visibility scope of the Post to one of options i:e. All, Followers, Follows, Self.
	• Post Owner can change the scope of post anytime later on edit of a post.
	• While displaying all the Posts on index page, we would filter posts based on post scope and state of current user.
	• Only the eligible post based on scope of the post set by the post owner will be available to view for any user.
	
## Details of Followers and Follows Users:
### SubDetails:
	• On profile page where we show count of followers and follows for that user, we would now also provide a hyperlink to view details of those followers/follows.
	• On click of that link, we route to a new template, which would give following details of each user i.e. username, total number of posts, total number of followers, total follows.
	• Username on this new page will be again a hyperlink, which would route to profile detail page of that user.
	
## Repost Feature:
###    SubDetails:
	• User who is not the owner of a post, will have the option to repost(like a retweet) any post visible to him/her.
	• User will be given a new hyperlink of repost in each post section on the index template.
	• On click of that hyperlink, user is routed to a new page, where the post content is prepopulated in a non editable text area, user cannot change the content of the post but can change the visibility scope of it.
	
## Search Post Feature:
###  SubDetails:
	•  On the top bar, we would introduce a new section for Search and it would be available to both loggedIn and nonLoggedIn users.
	• On click of it, user would be routed to a new search template which would have a input field to search with a username and also the calendars to search based on from and to date.
	• User can search posts from all the users in a given date frame, or search for posts from a particular user or combine both to search post from a particular user within a specific date frame. User can also search based on just one date from or to, if user does not enters any specific condition, then all the eligible posts will be loaded.
	• On click of search, user will be presented with the index page but with the filtered posts based on the above search  criteria.
	
## Message Feature:
###	SubDetails:
	•   On the top bar, we would introduce a new section for Message and it would be available only to loggedIn users.
	•  When user clicks on that, they can see all his/her inbox messages, and on top sub bar of message template, user would have the option to see       his/her sent messages and can compose a new message also.
	•  User will be presented with the reply option to his inbox messages.
	•  User need to add username of the recipient user, for sending a message and you can send message to only 1 recipient at a time.
	•  Already read messages would be greyed out.
	
## Celebrity Account:
###	SubDetails:
	•  Users with more than 10  followers will be considered as a celebrity.
	•  Celebrity Users username will be shown in golden color against all its post on index page.

## Mobile Responsive:
	•  Using Dev tools "Toggle Device toolbar" used simulator to ensure all the views are mobile responsive.
	

