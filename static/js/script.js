navbar = $(".navbar")

let theme = localStorage.getItem("theme") ? localStorage.getItem("theme") : "light"

$(window).on("load", ()=>{
    themeLoader(theme)
})

$(window).scroll(function() {
    var height = $(window).scrollTop();
    
    if(height > 475){
        navbar.css('padding-top', '1.5em')
        navbar.css('padding-bottom', '1.5em')
        navbar.css('padding-top', '1.5em')
        $(".navbar .btn-container").css('opacity', '1')
        $(".navbar .btn-container").css('pointer-events', 'all')

    }
    else {
        navbar.css('padding-top', '1.75em')
        navbar.css('padding-bottom', '1.75em')
        $(".navbar .btn-container").css('opacity', '0')
        $(".navbar .btn-container").css('pointer-events', 'none')
    }
})

$("#theme-switcher").on("click", ()=>{
    themeToggle()
})

function themeLoader(theme){
    if(theme=="light"){
        $(".navbar #theme-switcher .circle").css("right", "2px")
        $(".navbar #theme-switcher .circle").css("left", "unset")

        document.documentElement.style.setProperty("--background", "#f6f6f6");
        document.documentElement.style.setProperty("--white", "#0e0e0e");
        document.documentElement.style.setProperty("--convo-grey", "#ebebeb");
        document.documentElement.style.setProperty("--message-white", "#FFF");
        document.documentElement.style.setProperty("--background-image", "url('/static/res/logo-light.png')");
        document.documentElement.style.setProperty("--image", "url('/static/res/image-light.png')");
    } else {
        $(".navbar #theme-switcher .circle").css("left", "2px")
        $(".navbar #theme-switcher .circle").css("right", "unset")

        document.documentElement.style.setProperty("--background", "#131313");
        document.documentElement.style.setProperty("--white", "white");
        document.documentElement.style.setProperty("--convo-grey", "#1A1A1A");
        document.documentElement.style.setProperty("--message-white", "#e1e1e1");
        document.documentElement.style.setProperty("--background-image", "url('/static/res/logo.png')");
        document.documentElement.style.setProperty("--image", "url('/static/res/image.png')");
    }
}

function themeToggle(){
    if(theme=="dark"){
        localStorage.setItem("theme", "light")
        theme = "light" //toggling theme
        $(".navbar #theme-switcher .circle").css("right", "2px")
        $(".navbar #theme-switcher .circle").css("left", "unset")

        document.documentElement.style.setProperty("--background", "#f6f6f6");
        document.documentElement.style.setProperty("--white", "#0e0e0e");
        document.documentElement.style.setProperty("--convo-grey", "#ebebeb");
        document.documentElement.style.setProperty("--message-white", "#FFF");
        document.documentElement.style.setProperty("--background-image", "url('/static/res/logo-light.png')");
        document.documentElement.style.setProperty("--image", "url('/static/res/image-light.png')");
    } else {
        localStorage.setItem("theme", "dark")
        theme = "dark"
        $(".navbar #theme-switcher .circle").css("left", "2px")
        $(".navbar #theme-switcher .circle").css("right", "unset")

        document.documentElement.style.setProperty("--background", "#131313");
        document.documentElement.style.setProperty("--white", "white");
        document.documentElement.style.setProperty("--convo-grey", "#1A1A1A");
        document.documentElement.style.setProperty("--message-white", "#e1e1e1");
        document.documentElement.style.setProperty("--background-image", "url('/static/res/logo.png')");
        document.documentElement.style.setProperty("--image", "url('/static/res/image.png')");
    }
}