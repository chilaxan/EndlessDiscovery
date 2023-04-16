<script setup>
import pages from "./components/Pages.vue"

import {ref} from "vue";
import SiteViewer from "@/components/SiteViewer.vue";


const API_URL = "https://api.endlessdiscovery.tech/"
var currentView = ref("")
const refreshFrame = ref(false)

function newPage() {
    const data = {
        slug: pageName.value,
        description: pageDescription.value
    }
    const response = fetch(API_URL + "new", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).catch((error) => {
        console.error("Error creating page: " + error)
    }).then((response) => {
        window.location.hash = pageName.value
        window.location.reload()
        return response
    })
}
function revise() {
    const data = {
        slug: currentPage.value,
        revision: revision.value
    }
    if (revision.value === "" || revision.value === null) {
        alert("Revision cannot be empty")
        return;
    }
    const response = fetch(API_URL + "revise", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).catch((error) => {
        console.error("Error creating page: " + error)
    }).then((response) => {
        getDetails();
        revision.value = ""
        refreshFrame.value = !refreshFrame.value
        return response
    })
}
function getDetails() {
    const data = {
        slug: currentPage.value
    }
    const response = fetch(API_URL + "details", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).catch((error) => {
        console.error("Error creating page: " + error)
    }).then(async (response) => {
        currentView.value = await response.json()
        currentView.value.revisions = currentView.value.revisions.reverse()
        currentView.value.revisions = currentView.value.revisions.slice(0, 6)

    })
}
var pageDescription = ref("")
var pageName = ref("")
var currentPage = ref("")
var revision = ref("")
currentPage.value = window.location.hash.substring(1)
if (currentPage.value !== "") {
    getDetails()
}
function cleanDescription(desc) {
    if (desc.length > 150) {
        return desc.substring(0, 150) + "..."
    } else {
        return desc
    }
}
</script>

<template>
    <div class="h-full">
        <div class="inline-flex w-full bg-slate-700 text-white bg-gradient-to-r from-slate-700 to-violet-950">
            <div class="p-5">
                <a href="/">
                    <img
                        class="inline aspect-square w-32 ml-auto mx-4 hover:animate-ping"
                        src="https://cdn.discordapp.com/attachments/1095864447026856197/1097025342738272377/endlessdiscovery.png" alt="Endless Discovery"
                    >
                    <div class="inline-block mt-auto align-middle">
                        <span class=" text-4xl">Endless Discovery</span>
                        <br>
                        <span class=" text-md pt-2 italic">Explore the Infinite Possibilities</span>
                    </div>
                </a>
                <br>
                <a
                    v-if="!(currentPage.trim().length === 0 || currentPage === '/')"
                    class="text-2xl"
                    :href="'/' + currentPage"
                >[{{currentPage}}]</a>
            </div>
        </div>
        <div
            v-if="(currentPage.trim().length === 0 || currentPage === '/')"
        >
        <div class="w-full">
            <div class="bg-slate-200 mt-10 mx-4 rounded-xl p-6">
                Welcome to Endless Discovery, a website that offers a endless supply of captivating content for you to explore.
                With our diverse range of topics and endless stream of fresh content, you'll never run out of things to
                discover. From fascinating stories to thought-provoking articles, we have it all. Join us on a journey of
                endless exploration and uncover the infinite possibilities that await!
            </div>
        </div>
            <div class="inline-flex w-full">
                <div class="bg-slate-200 mt-10 w-1/2 mx-4 rounded-xl">
                    <h1 class="font-bold text-lg text-center"> Create your own page</h1>
                    <form class="m-3">
                        <div class="flex">
                            <label class="flex-auto" for="pageName">Page Name</label>
                            <input
                                class="w-4/6 h-10"
                                v-model="pageName"
                                type="text"
                                id="pageName"
                                name="pageName"
                                placeholder="Page Name"
                            >
                        </div>
                        <div class="flex mt-4">
                            <label class="flex-auto" for="pageDescription">Page Description</label>
                            <input class="w-4/6 h-10"
                                   v-model="pageDescription"
                                   type="text"
                                   id="pageDescription"
                                   name="pageDescription"
                                   placeholder="Page Description">
                        </div>
                        <button class="bg-violet-300 text-black w-full h-10 mt-4" type="submit"
                                @click.prevent="newPage(pageName, pageDescription)">Create Page
                        </button>
                    </form>
                </div>
                <div class="bg-slate-200 mt-10 w-1/2 mx-4 rounded-xl">
                    <suspense>
                        <pages></pages>
                    </suspense>
                </div>
            </div>
        </div>
        <div class="flex h-4/5" v-if="!(currentPage.trim().length === 0 || currentPage === '/')">
            <SiteViewer
                class="inline-flex"
                :page="'https://endlessdiscovery.tech/' + currentPage"
                :key="refreshFrame"
            >
            </SiteViewer>
            <div
                class=" bg-slate-400 min-h-screen w-96 text-center"
            >
                <h1 class="py text-lg font-bold">Site Info</h1>
                <span><b>Name</b>:<br> {{currentView.slug}}</span>
                <br>
                <span><b>Description</b>:<br> {{currentView.description}}</span>
                <span></span>
                <h1 class="py-3 text-lg font-bold">Revise this site</h1>
                <form class="m-3">
                    <textarea class="w-5/6 h-16"
                           v-model="revision"
                           type="text"
                           id="revision"
                           name="revision"
                           placeholder="Describe the changes">
                    </textarea>
                    <button class="bg-violet-300 text-black w-full h-10 mt-4" type="submit"
                            @click.prevent="revise()">Revise Page
                    </button>
                </form>
                <br>
                <h1 class="py-2 text-lg font-bold">Previous Revisions</h1>
                <div
                    v-for="revision in currentView.revisions"
                    class="overflow-ellipsis overflow-hidden bg-blue-200/20 py-2 m-2 rounded-md"
                    :key="revision">
                    {{cleanDescription(revision)}}
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
</style>
