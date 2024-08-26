from flask import Flask,render_template,request,url_for,redirect
from serpapi import GoogleSearch
item=["Blue Shirt","Red Shirt","Black Pants","Watch"]

app = Flask(__name__)


web_name="Shopsmart"

dis=[]

def get_title(ite):
    params = {
    "engine": "walmart",
    "query": ite,
    "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"][2]["title"]
    return organic_results

def fetch_image(query):
    params = {
        "engine": "google_images",
        "q": query,
        "location": "Austin, TX, Texas, United States",
        "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract the URL of the first image
    if "images_results" in results and len(results["images_results"]) > 0:
        return results["images_results"][0].get("thumbnail")  # or use "original" if you need the full-sized image
    return None

one_image_per_query = {}

for query in item:
    # print(f"Fetching image for: {query}")
    one_image_per_query[query] = fetch_image(query)
    dis.append(get_title(query))

img_url=[]

# Print the collected image URLs
for query, image_url in one_image_per_query.items():
    if image_url:
        img_url.append(image_url)
        # print(f"\nImage for query '{query}': {image_url}")
    else:
        print(f"\nNo image found for query '{query}'")

# @app.route("/")
# def hello_world():
# #     return render_template("index.html",web_name=web_name)
# print("It worked correctly")
# print(image_url[1])

@app.route("/")
def index():
    combin=list(zip(item,img_url,dis))
    print(combin)
    return render_template("index.html",name=web_name,item=item,img_url=img_url,combin=combin)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/checkout/<product>/")
def checkout(product):
    return render_template("checkout.html",product=product)



@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       email=request.form.get("email")
       text=request.form.get("text")
       message=request.form.get("message")
       print(text+"\n"+email+"\n"+message)
       return redirect("/thanks")
    return render_template("contact.html")

@app.route("/thanks")
def feed():
    return render_template("thanks_feed.html")

@app.route("/thanksbye")
def bought():
    return render_template("bought.html")



def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(debug=True)