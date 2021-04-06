<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <AhfezVmodel v-model="whatInput"/>
    <input type="text" :disabled="figer"> 
  </div>
</template>

<script>

// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import AhfezVmodel from '../components/AhfezVmodel.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld , AhfezVmodel
  },
  data(){
    return{
      whatInput:'',
      figer:false
    }
  },
  mounted(){
    alert("ready")
  }
}
</script>
