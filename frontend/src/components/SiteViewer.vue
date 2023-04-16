<script>
import {watch} from "vue";

export default {
    name: "SiteViewer",
    props: {
        page: {
            type: String,
            required: true
        },
        refr: {
            type: Boolean,
            required: false
        }
    }
}
console.log("SiteViewer loaded")
</script>

<template>
    <div class="block w-full">
        <iframe
                class="h-full w-full"
                :src="page"></iframe>
    </div>
</template>
<style scoped>
</style>