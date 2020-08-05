window.onload = function () {
  //Clear the session Data to have inbox as default view on reloads
  sessionStorage.setItem("load", null);
}

//Use buttons to toggle between views
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#inbox').addEventListener('click', () => load_messagebox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_messagebox('sent'));
  document.querySelector('#compose').addEventListener('click', compose_message);
  if (sessionStorage.getItem("load") == null || sessionStorage.getItem("load") == "null") {
    //By default, load the inbox
    load_messagebox('inbox');
  } else if (sessionStorage.getItem("load") == "reply") {
    //Load Reply Content on Compose View
    manageView('block', 'none', 'none');
    reply_content(sessionStorage.getItem("messageObject"));
  } else if (sessionStorage.getItem("load") == "sent") {
    //Load Sent mailbox after sending from compose
    load_messagebox('sent');
  } else {
    //Load inbox by as  default view
    manageView('none', 'none', 'block');
  }
}, { once: true });

//Show compose view and hide other views
function compose_message() {
  sessionStorage.setItem("load", null);
  manageView('block', 'none', 'none');
  //Clear out compose fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('form').onsubmit = sendMessage;
}

//Show the mailbox and hide other views
function load_messagebox(mailbox) {
  sessionStorage.setItem("load", null);
  manageView('none', 'none', 'block');
  let url = "/messages/" + mailbox;
  fetch(url)
    .then(response => response.json())
    .then(messages => {
      populateMessageList(messages, mailbox);
    });
}

//Load the content of the selected email with passed Id
function loadMessageContent(id, mailtype) {
  if (mailtype === "inbox") {
    document.querySelector('#reply').style.display = 'block';
  } else {
    document.querySelector('#reply').style.display = 'none';
  }
  manageView('none', 'block', 'none');
  let url = "/messagecontent/" + id;
  fetch(url)
    .then(response => response.json())
    .then(message => {
      document.querySelector('#mail-body').innerHTML = message.content;
      document.querySelector('#reply').addEventListener('click', () => reply_message(message));
    });
}

//Populate mail box with mail content
function populateMessageList(massageList, mailType) {
  var table = document.getElementById("mailbox");
  var rowCount = table.rows.length;
  for (var i = 1; i < rowCount; i++) {
    table.deleteRow(1);
  }
  massageList.forEach(function (item) {
    let newRow = table.insertRow();
    newRow.setAttribute("id", item.id, 0);
    let fromCell = newRow.insertCell(0);
    let fromText = document.createTextNode(item.sender);
    fromCell.appendChild(fromText);
    let toCell = newRow.insertCell(1);
    let toText = document.createTextNode(item.creation_time);
    toCell.appendChild(toText);
    newRow.style.borderBottom = "thin solid";
    if (item.read) {
      newRow.style.backgroundColor = "#D3D3D3";
    } else {
      newRow.style.backgroundColor = "#FFFFFF";
    }
  });
  addRowHandlers(mailType);
}

//Send Message
function sendMessage() {
  var recipient = document.getElementById("compose-recipients").value;
  var body = document.getElementById("compose-body").value;
  fetch('/sendmessage', {
    method: 'POST',
    body: JSON.stringify({
      recipient: recipient,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log('Message Sent Successfully');
    })
    .catch(error => {
      console.log('Error while Sending a Message');
    });
  sessionStorage.setItem("load", "sent");
}

//Open a Content of an Message on click of any message. 
function addRowHandlers(mailType) {
  var table = document.getElementById("mailbox");
  var rows = table.getElementsByTagName("tr");
  for (i = 1; i < rows.length; i++) {
    var currentRow = table.rows[i];
    var createClickHandler = function (row) {
      return function () {
        loadMessageContent(this.id, mailType);
      };
    };
    currentRow.onclick = createClickHandler(currentRow);
  }
}

//Set the Reply data to session object to be used on domcontentLoader event.
function reply_message(messageObject) {
  sessionStorage.setItem("load", "reply");
  sessionStorage.setItem("messageObject", JSON.stringify(messageObject));
}

//Prepopulate reply email content and handle submission of reply.
function reply_content(messageObject) {
  messageObject = JSON.parse(messageObject);
  document.querySelector('#heading').innerHTML = "Reply Message";
  document.querySelector('#compose-recipients').value = messageObject.sender;
  document.querySelector('#compose-body').value = "On  " + messageObject.creation_time + "   " + messageObject.sender + " wrote: " + "\n" + messageObject.content;
  sessionStorage.setItem("load", "reply");
  sessionStorage.setItem("messageObject", JSON.stringify(messageObject));
  document.querySelector('form').onsubmit = sendMessage;
}

// Manage different views displays.
function manageView(composeView, contentView, emailView) {
  document.querySelector('#compose-view').style.display = composeView;
  document.querySelector('#mail-content-view').style.display = contentView;
  document.querySelector('#emails-view').style.display = emailView;
}




