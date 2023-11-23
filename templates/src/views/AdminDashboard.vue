<template>
  <div class="admin" v-if="admin">
    <header>

<ul class="navi_links">
      <h1>Welcome Admin</h1>
      <li><a>{{ admin.username }}<p>@email:{{ admin.email }}</p></a></li>
      <li><a><router-link :to="{ name: 'SummaryPage', params: { id:admin.id }}">Summary</router-link></a></li>
      <li><a @click="logout()">Logout</a></li> 
</ul>
</header>
    <br>
    <div class="venues" v-if="venue">
      <button class="button" style="vertical-align:middle" ><span><router-link   :to="{ name: 'NewVenue', params: { admin_id: admin.id }}">+ VENUE</router-link></span></button>
      <div class="each_venue" v-for="venues in venue"   :key="venues.id">
        <div class="venue-box">
          <h3 class="venues-name">{{ venues.name }}</h3>
          <button class="button-35" role="button" @click="trigger_celery_job(venues.id)" >Export csv</button>
          <br>
          <button class="sbutton"><span><router-link   :to="{ name: 'NewShow', params: { venue_id: venues.id, admin_id:admin.id }}">+ SHOW</router-link></span></button>
          <div class="venues-button"  data-inline="true" >
          <button class="edit-button" ><a><router-link :to="{ name: 'UpdateVenue', params: { venue_id: venues.id, admin_id:admin.id }}">Edit</router-link></a></button>
          <button  class="delete-button"  data-inline="true" @click="deleteVenue(venues.id)"><a>Delete</a></button>
        </div>
          <div class="venuecon">

    <div class="show-box" v-for="shows in venues.shows" :key="shows.show_id">
          <h3>{{ shows.name }}</h3>
          <img class="show-img" v-bind:src="getImageUrl(shows.image_file)" alt="Description of the image">
		<div class="show-container" data-inline="true">
          <button ><router-link :to="{ name: 'UpdateShow', params: { venue_id: venues.id,show_id:shows.id,admin_id:admin.id }}">Edit</router-link></button>
			<button @click="deleteShow(venues.id,shows.id)"><a>Delete</a></button>
		</div>
  </div>
        </div>
        <br>
        </div>
        <br>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name:"AdminDashboard",
    data() {
      return {
      admin: null,
      venue:null,
      error: null,
    };
  },
  mounted() {
    this.fetchAdmin();
    this.fetchVenue();
  },
  methods: {
    trigger_celery_job(venue_id){
      fetch(`http://127.0.0.1:5000/${venue_id}/trigger_job/celery`)
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log("Task success:",result.Task_state)
          let interval = setInterval(() =>{
            fetch(`http://127.0.0.1:5000/status/${result.Task_id}`).then(r => r.json())
            .then(d=>{
              if(d.Task_state === "SUCCESS"){
                console.log("Task has finished execution")
                clearInterval(interval);
                window.location.href = `http://127.0.0.1:5000/download/${result.Task_id}`;
              }else {
                console.log("Task is still being executed....")
              }
            })
          },4000); 
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    getImageUrl(imageFile) {
      return require(`../assets/images/${imageFile}`)
    },
    fetchAdmin() {
      const admin_id = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/api/${admin_id}/admin`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result); // Log the entire result object
          if (result && result.email && result.id && result.username) {
            this.admin = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    fetchVenue(){
      fetch(`http://127.0.0.1:5000/api/get/venue`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            console.log(response)
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result); // Log the entire result object
          if (result) {
            this.venue = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    deleteVenue(venue_id){
      if(confirm("Do you really want to delete this venue?")){
      fetch(`http://127.0.0.1:5000/api/${venue_id}/delete/venue`, {
        method: 'DELETE',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            console.log(response)
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result); // Log the entire result object
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
      }
    },
    
    deleteShow(venue_id,show_id){
      if(confirm("Do you really want to delete this show?")){
      fetch(`http://127.0.0.1:5000/api/${venue_id}/${show_id}/delete/show`, {
        method: 'DELETE',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            console.log(response)
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result); // Log the entire result object
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
      }
    },
    logout() {
      // Send the login request to the server
      fetch(' http://127.0.0.1:5000/api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
      })
        .then(response => response.json())
        .then(result => {
          console.log(result);
          if (result.message === 'Logged out') {
            console.log("Logout successful");
            localStorage.setItem('token', "null");
            this.$router.push(`/login`);
          } else {
            console.log("Logout failed");
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
};

</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lato', 'Arial', sans-serif;
}
header{
display:flex;
justify-content:flex-end;
align-items:center;
padding:10px 10%;
background-color:#000;
}
.logo {
cursor:pointer;
margin-right:auto;
}
.navi_links{
list-style:none;
}
.navi_links li{
display:inline-block;
padding:10px 10px;
}
.navi_links h1{
  font-size: 40px;
  float: left;
  margin-right: 700px;
  color:white;
  font-family:fantasy;
}
.navi_links h1 p{
  font-size: 15px;
}
.navi_links li a{
transition:all 0.3s ease 0s;
color:#FFFFFF;
}
.navi_links li a:hover{
color:#0088a9
}
.button-35 {
  align-items: center;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: transparent 0 0 0 3px,rgba(18, 18, 18, .1) 0 6px 20px;
  box-sizing: border-box;
  color: #121212;
  cursor: pointer;
  display: inline-flex;
  flex: 1 1 auto;
  font-family: Inter,sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  justify-content: center;
  line-height: 1;
  float: right;
  outline: none;
  padding: 1rem 1.2rem;
  text-align: center;
  text-decoration: none;
  transition: box-shadow .2s,-webkit-box-shadow .2s;
  white-space: nowrap;
  border: 0;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button-35:hover {
  box-shadow: #121212 0 0 0 3px, transparent 0 0 0 0;
}
.sbutton {
  display: inline-block;
  border-radius: 4px;
  background-color: #f4511e;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 22px;
  text-decoration: none;
  padding: 10px;
  width: 200px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}

.sbutton span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
  text-decoration: none;
}

.sbutton span:after {
  content: '\00bb';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.sbutton:hover span {
  padding-right: 25px;
}

.sbutton:hover span:after {
  opacity: 1;
  right: 0;
}
.button {
  display: inline-block;
  border-radius: 4px;
  background-color: #f4511e;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 28px;
  padding: 20px;
  width: 200px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}

.button span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  text-decoration: none;
  transition: 0.5s;
}

.button span:after {
  content: '\00bb';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.button:hover span {
  padding-right: 25px;
}

.button:hover span:after {
  opacity: 1;
  right: 0;
}
h1{
  margin-right:700px;
}
.venues{
  display: flex;
  flex-direction:column;
}
.venue-box{
  margin: 20px;
  padding: 10px;
  background: url('../assets/3d.jpg');
  border-radius: 10px;
}

.venue-box .sbutton{
  margin-right:100px;
}
.venuecon{
  display:flex;
}
.venues-name {
  font-size: 40px;
  margin-left:0px;
  margin-right:70px;
  text-align:center;
  color:#FFFFFF;
}
.venues-description {
  font-size: 1rem;
  margin: 1px;
}

.venues-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  margin-left:10px;
}

.edit-button{
  background-color: #ccc;
  border: none;
  border-radius: 3px;
  color: #000;
  text-decoration:none;
  font-size: 1rem;
  justify-content: space-between;
  padding: 12px 12px;
  margin-left: 0px;
  margin-right:500px;
  cursor: pointer;
  margin-bottom:20px;
}
.delete-button {
  background-color: #ccc;
  border: none;
  border-radius: 3px;
  color: #000;
  text-decoration:none;
  font-size: 1rem;
  justify-content: space-between;
  padding: 12px 12px;
  margin-left: 500px;
  margin-right:0px;
  cursor: pointer;
  margin-bottom:20px;
}
.edit-button:hover, .delete-button:hover {
  background-color: #666;
}
.show-box {
	width: 250px;
	height: 410px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
	display: flex;
	flex-direction: column;
	justify-content: space-around;
  background: #000;
  position:relative;
	}
  .show-container {
  width: 100%;
  height: 100%;
  top:0;
  right:0;
  position:absolute;
  background: #00000013;
  backdrop-filter: blur(0px);
  border-radius:15px;
  color:#fff;
  padding:30px;
  justify-content: space-around;
  /* display: flex;
  flex-direction: column;
  justify-content: space-between; */
  transition:2s;
	}
  .show_box:hover .show-container{
    right:0;
  }
		.show-container button {
			padding: 5px 5px;
			font-size: 1.2rem;
			background-color: #4CAF50;
			color: white;
			border: none;
			border-radius: 5px;
			cursor: pointer;
			margin-top:300px;
		}
		.show-container button:hover {
			background-color: #3e8e41;
		}  
</style>
   
