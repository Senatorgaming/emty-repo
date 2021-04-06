<template>
  <div class="about">
    <h1>This is an about page</h1>
    <EmitModel v-model="coupon"/>
  </div>
</template>
<script>
import EmitModel from "../components/EmitModel";
export default {
  name:"about",
  components:{EmitModel},
  data(){
    return{
      coupon:'my name is armia'
    }
  }
}
</script>
