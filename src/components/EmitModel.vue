<template>
  <input :value="value" @input="updateCode($event.target.value)" ref="input">
</template>

<script>
export default {
    props: ["value"],
    data(){
        return{
            invalid:['ALLFree', 'somethingelse']
        }
    },
    methods:{
        updateCode(armia){
            if(this.invalid.includes(armia)){
                alert("This coupon is no longer valid, sorry!") 
                armia = ''  
            }
            this.$emit('input', armia)
        }
    }
}
</script>

<style>

</style>
