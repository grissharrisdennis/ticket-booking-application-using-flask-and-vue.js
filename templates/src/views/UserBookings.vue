<template>
  <div class="userbook">
    <header>
    <ul class="nav_links">
      <li><h2>User Bookings</h2></li>
      <li><a ><router-link   :to="{ name: 'UserDashboard', params: { id:this.$route.params.id }}">UserDashboard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>
    </ul>
</header>
</div>


<div class="con" v-for="books in book" :key="books.booking_id">
  <div class="b" v-for="venues in venue"   :key="venues.id">
    <div class="v" v-if="books.venue_id==venues.id">
      <div v-for="show in venues.shows" :key="show.id">
    <div class="containers" v-if="books.show_id==show.id">
<div class="cardn card-left" >
  <br>
    <h1>{{ show.name }}</h1>
    <br>
    <h2>{{ venues.name }}</h2>
    <br>   
    <h4>{{ show.show_time }}</h4>
    <br>
    <star-rating v-model:rating="rating" />
    <button class="postrate" @click="postRating(show.id)">Submit Rating</button>
</div>
<div class="cardn card-right">
  <div class="number">
  <span>SEATS</span>
  <br>
  <br>
    <h3>{{ books.seats}}</h3>
    <br>
    <div>
  </div>  
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</template>

<script>
import StarRating from 'vue-star-rating'

export default {
    name:'  UserBookings',
    components: {
      StarRating,
  },
    data() {
      return {
      admin: null,
      venue:null,
      book: null,
      rating:'',
    };
},
mounted() {
    this.fetchbooking();
    this.fetchVenue();
  },
    methods:{
      postRating(show_id){
         const data={
          rating:this.rating,
         }
         const id=this.$route.params.id
         fetch(`http://127.0.0.1:5000/api/post/${id}/${show_id}/rating`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify(data),
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
          console.log(result); // Log the entire result object\
          this.rating = result.rating
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
  
    fetchbooking(){
        const id=this.$route.params.id;
      fetch(`http://127.0.0.1:5000/api/${id}/get/bookings`, {
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
            this.book = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
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
    
    }
    
}
</script>

<style>
.postrate{
  border-radius: 12px;
  background: #525252;
  padding:10px;
}
.nav_links h2{
  color:#fff;
}
.containers{
    width:30em;
    margin-left:30px;
    font-family:sans-serif;
    display:flex;
    flex-wrap:wrap;
}
.cardn {
    background:linear-gradient(to bottom ,black 0%,black 26%,#ecedef 26%,#ecedef 100%);
    height:16em;
    padding:1em;
    float:left;
    position:relative;
    margin-top:100px;
}
.card-left{
    border-top-left-radius:8px;
    border-bottom-left-radius:8px;
    width:19em;
}
.card-right{
    width:6.5em;
    border-left:0.18em dashed #fff;
    border-top-left-radius:8px;
    border-bottom-left-radius:8px;
}
.card-right::before,.card-right::after{
    width:0.9em;
    height:0.9em;
    background-color:#fff;
    content:"";
    position:absolute;
    display:block;
    border-radius:50%;
    left:-0.5em;
}
.card-right::before{
    top:-0.4em;
}
.card-right::after{
    bottom:-0.4em;
}
        h1{
        font-size:1.0em;
        margin-top:0;
        color:#fff;
        width: 100%;
        }
        h1 span{
        font-weight:normal;
        }        
        .title,
        .name,
        .seat,
        .time{
        text-transform:uppercase;
        font-weight:normal;
        }
        .title h2,
        .name h2,
        .seat h2,
        .time h2{
        font-size:0.7em;
        color:#525252;
        margin:0;
        }
        .title span ,
        .name span,
        .seat span,
        .time span{
        font-size:0.5em;
        color:#a2aeae;
        }
        .title{
         margin:2em 0 0 0;
        }
        .name
        .seat{
         margin:0.7em 0 0 0;
        }
        .time{
        margin:0.7em 0 0 0;
        }
        .time,
        .seat{
        float:left;
        }
        .eye{
        position:relative;
        width:2em;
        height:1.5em;
        background:#fff;
        margin:0 auto;
        border-radius:1em/0.6em;
        z-index:1;
        }
        .eye::before,
        .eye::after{
        content:"";
        display:block;
        position:absolute;
        border-radius:50%;
        }
        .eye::before{
        width:1em;
        background:#3dcee8;
        height:1em;
        z-index:2;
        left:8px;
        top:4px;
        }
        .eye::after{
        width:0.5em;
        background:#fff;
        height:0.5em;
        z-index:3;
        left:12px;
        top:8px;
        }
        .number{
        text-transform:uppercase;
        text-align:center;
        }
        .number h2{
        color:#2980B9;
        margin:0.9em 0 0 0;
        font-size:2.5em;
        }
.number span{
    display:block;
    color:#a2aeae;
}
</style>