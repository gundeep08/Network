//Manage Likes and Dislikes to a Post
function manageLike(postId) {
  var originalLikes=document.getElementById(postId).innerHTML;
  originalLikesCount=parseInt(originalLikes);
  fetch(`/manageLike/${postId}`)
  .then(response => response.text())
  .then(text => {
      if(text =="delete"){
          let newLikeCount= originalLikesCount-1;
          document.getElementById(postId).innerHTML=newLikeCount;
      }else if(text =="add"){
          let newLikeCount= originalLikesCount+1;
          document.getElementById(postId).innerHTML=newLikeCount;
      }
  });
  }

//Update both follow/unfollow options based on user selection
  function manageFollow(postOwnerId) {
     var followers=parseInt(document.querySelector("#followers").textContent);
     if(document.getElementById("follow").value=="Follow"){
         let url = "/follow/" + postOwnerId;
         fetch(url)
         .then(response => response.text())
         .then(text => {
             let newFollower=followers+1;
             document.querySelector("#followers").textContent=newFollower;
             document.getElementById("follow").value="Unfollow";
         });
     }else if(document.getElementById("follow").value=="Unfollow"){
         let url = "/unfollow/" + postOwnerId;
         fetch(url)
         .then(response => response.text())
         .then(text => {
             let newFollower=followers-1;
             document.querySelector("#followers").textContent=newFollower;
             document.getElementById("follow").value="Follow";
     });
     }
 }