from flask import Flask, jsonify,request 
from flask_cors import CORS
from datetime import datetime, timezone

import json

app = Flask(__name__)
CORS(app)

ISSUES = []
next_id = 1

def gnid():
    global next_id
    result = next_id
    next_id += 1
    return result




def current_time():
    return datetime.now(timezone.utc).isoformat()

def make_issue(title, description="", status="open", priority="medium", assignee=None):
    iid = gnid()
    item = {
        "id": iid,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "assignee": assignee ,
        "created_at": current_time()  ,
       
    }
    ISSUES.append(item)
    return item

#dummy issues

make_issue("login err", "throws 500 when submit", status="open")
make_issue("pg fail", "502 sometimes", priority="high")
make_issue("navbar", "not responsive on mobile", assignee="priyanka")




@app.route("/issues", methods=["GET"])
def list_issues():
    q = request.args.get("q", default=None, type=str)
    status = request.args.get("status", default=None, type=str)
    priority = request.args.get("priority", default=None, type=str)
    assignee = request.args.get("assignee", default=None, type=str)
    sort_by = request.args.get("sortBy", default=None, type=str) 
    sort_dir = request.args.get("sortDir", default="asc", type=str)

#pagination

    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
    except ValueError:
        page, page_size = 1, 10
    if page < 1: page = 1
    if page_size < 1: page_size = 10


    items = ISSUES
    if q:
        items = [i for i in items if q.lower() in i["title"].lower()]
    if status:
        items = [i for i in items if i["status"] == status]

    if priority:
        items = [i for i in items if i["priority"] == priority]

    if assignee:
        items = [i for i in items if i.get("assignee") and assignee.lower() in i["assignee"].lower()]

    total = len(items)

    if sort_by:
        reverse = (sort_dir == "desc")
        items = sorted(items, key=lambda x: x.get(sort_by) or "", reverse=reverse)

    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]

    return jsonify({
        "data": page_items,
        "meta": {
            "total": total,
            "page": page,
            "pageSize": page_size,
            "totalPages": (total + page_size - 1) // page_size
        }
    })

   

    


@app.route("/issues/<int:iid>", methods=["GET"])
def get_issue(iid):
    item = next((x for x in ISSUES if x["id"] == iid), None)
    if not item:
        return jsonify({"not found"}), 404
    return jsonify(item)


@app.route("/issues", methods=["POST"])
def add_issue():
    body = request.json
    if not body or "title" not in body:
        return {"error": "title??"}, 400

    newi = {
        "id": gnid(),
        "title": body["title"],
        "description": body.get("description", ""),
        "status": body.get("status", "open"),
        "priority": body.get("priority", "medium"),
        "assignee": body.get("assignee"),
        "created_at": current_time()
    }

    ISSUES.append(newi)
    print("added issue:", newi)  # debug log
    return jsonify(newi), 201

@app.route("/issues/<int:iid>", methods=["PUT"])
def upd(iid):
    body = request.json
    for i in ISSUES:
        if i["id"] == iid:
            for k in body:
                i[k] = body[k]
            i["updated_at"] = current_time()
            return jsonify(i)
    return {"err": "no such issue"}, 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)