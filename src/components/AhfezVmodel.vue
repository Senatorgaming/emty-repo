<template>
<div>
    <input type="text" :value='value' @input="$emit('input', $event.target.value)">
     <ol>
        <li v-for="task in tasks" :key="task">{{task.description}}</li>
    </ol>
    <ol>
        <li v-for="task in incomplete" :key="task">{{task.description}}</li>
    </ol>
</div>
</template>
<script>
export default {
    props:["value"],
    data(){
        return {
            tasks: [
                {
                    description: 'go to school', completed:false
                },
                {
                    description: 'made diner', completed:true

                },

                {   description: 'wosh closhs', completed:false}
                ,
                {
                    description: 'go to chusrch', completed:true

                }


            ]
        }
    },
    computed: {
        incomplete(){
            return  this.tasks.filter(item => !item.completed)
        }
    }
}
</script>