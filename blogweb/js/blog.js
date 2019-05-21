function upload() {
    var form = new FormData();
    f = document.getElementById("upload-file")
    form.append("file", f.files[0]);
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            f.outerHTML = f.outerHTML
        } else if (req.readyState == 4 && req.status != 200) {
            alert("upload fail:" + req.responseText)
        }
    }
    req.open("post", "/upload", true);
    req.send(form);
}

function update() {
    var req = new XMLHttpRequest();
    req.open("post", "/update", true);
    req.send();
}

function articles() {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var articles = JSON.parse(req.responseText)
            var parent = document.getElementById("article-archives")
            for (var i = 0; i < articles.length; i++) {
                var article = articles[i]
                var div = document.createElement("div")
                div.className = "blog-post"
                var title = document.createElement("h2")
                title.className = "blog-post-title"
                title.innerHTML = article.title
                var meta = document.createElement("p")
                meta.className = "blog-post-meta"
                meta.innerHTML = article.date
                var snapshot = document.createElement("p")
                var a = document.createElement("a")
                a.href = "/html/page.html?name=" + article.title
                a.target = "_blank"
                a.innerHTML = article.snapshot
                snapshot.appendChild(a)
                div.appendChild(title)
                div.appendChild(meta)
                div.appendChild(snapshot)
                parent.appendChild(div)
            }
            var nav = document.createElement("nav")
            var ul = document.createElement("ul")
            ul.className = "pager"
            var previous = document.createElement("li")
            var a1 = document.createElement("a")
            a1.innerHTML = "Previous"
            previous.appendChild(a1)
            var next = document.createElement("li")
            var a2 = document.createElement("a")
            a2.innerHTML = "Next"
            next.appendChild(next)
            ul.appendChild(previous)
            ul.appendChild(next)
            nav.appendChild(ul)
            parent.appendChild(nav)
        }
    }
    req.open("get", "/articles", true);
    req.send();
}

function loadpage() {
    var url = location.search
    var name = ""
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            if (strs[i].split("=")[0] == "name") {
                name = unescape(strs[i].split("=")[1]);
            }
        }
    }
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            document.getElementById("page-body").innerHTML = req.responseText
        }
    }
    req.open("get", "/article/" + name, true);
    req.send();
}