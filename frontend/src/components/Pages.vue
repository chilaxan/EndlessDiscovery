

<script setup>

import {ref} from "vue";

const API_URL = "https://api.endlessdiscovery.tech/"

const GET = async (url) => {
    const response = await fetch(API_URL + url)
    console.log(url)
    return await response.json();
}
let list = ref([]);
let currentPage = ref(0);

list = await GET(`list?page=${currentPage.value}&count=4`)

const DELETE = async (url) => {
    console.log("Deleting page: " + url)
    const data = {
        "slug": url
    }
    const response = await fetch(API_URL + "delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then((response) => {
        return response
    }).catch((error) => {
        console.error("Error deleting page: " + error)
    })
}
function updateParent(slug) {
    window.location.hash = slug;
    window.location.reload();
}
function deletePage(slug, fu) {
    DELETE(slug)
    list = list.filter((item) => item.slug !== slug)
    fu()
}

function cleanDescription(desc) {
    if (desc.length > 150) {
        return desc.substring(0, 150) + "..."
    } else {
        return desc
    }
}
async function changePage(num, forceUpdate) {
    currentPage.value = Math.max(0, currentPage.value + num)
    let newList = await GET(`list?page=${currentPage.value}&count=4`)
    if (newList.length === 0) {
        currentPage.value = Math.max(0, currentPage.value - num)
    } else {
        list = newList
    }
    forceUpdate()
    console.log(list)
}
</script>

<script>
</script>
<template>
    <h1 class="font-bold text-lg text-center my-2">View Other Pages</h1>
    <div class="text-center">
        <h1 class="font-bold text-md text-center my-2"></h1>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                 class="w-10 h-10 bg-slate-400 mx-2 inline float-left"
                 @click="changePage(-1, $forceUpdate)">
            >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18" />
            </svg>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
             class="w-10 h-10 bg-slate-400 mx-2 inline float-right"
              @click="changePage(1, $forceUpdate)">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
        </svg>

    </div>
    <div class="grid grid-cols-2 mb-4">
    <div class="bg-slate-300 flex-col mx-3 my-1" v-for="item in list" :key="item.slug">
        <div class="w-full h-full">
            <div class="bg-red-500 w-7 aspect-square text-center cursor-pointer" @click="deletePage(item.slug, $forceUpdate)">X</div>
            <span class="block text-center font-bold cursor-pointer" @click="updateParent(item.slug)">{{item.slug}}</span>
            <span class="block text-center cursor-pointer" @click="updateParent(item.slug)">{{cleanDescription(item.description)}}</span>
        </div>
    </div>
  </div>
</template>
<style scoped>

</style>