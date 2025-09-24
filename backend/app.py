from flask import Flask, jsonify,request 
from flask_cors import CORS
from datetime import datetime
import itertools

app = Flask(__name__)
CORS(app)

ISSUES = []
next_id = 1

def get_next_id():
    global next_id
    result = next_id
    next_id += 1
    return result


from datetime import datetime, timezone

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def make_issue(title, description="", status="open", priority="medium", assignee=None):
    iid = next(next_id)
    item = {
        "id": iid,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "assignee": assignee ,
        "created_at": now_iso() ,
       
    }
    ISSUES.append(item)
    return item

make_issue("Login page error", "500 when submitting login", status="open", priority="high", assignee="Riya")
make_issue("Add unit tests for auth", "Write pytest tests", status="in_progress", priority="medium", assignee="Amit")
make_issue("Refactor navbar", "Make it responsive", status="open", priority="low", assignee="Riya")
make_issue("Payment gateway failing", "Intermittent 502", status="open", priority="high", assignee="Suresh")
make_issue("Remove deprecated API", "Cleanup old endpoint", status="closed", priority="medium", assignee=None)


def apply_search(items, q):
    if not q:
        return items
    q = q.lower()
    return [i for i in items if q in (i.get("title","").lower())]


def apply_filters(items, status=None, priority=None, assignee=None):
    result = items
    if status:
        result = [i for i in result if str(i.get("status")) == str(status)]
    if priority:
        result = [i for i in result if str(i.get("priority")) == str(priority)]
    if assignee:
        if assignee.lower() in ("null","none","unassigned",""):
            result = [i for i in result if not i.get("assignee")]
        else:
            al = assignee.lower()
            result = [i for i in result if i.get("assignee") and al in i.get("assignee","").lower()]
    return result


def apply_sort(items, sort_by=None, sort_dir="asc"):
    if not sort_by:
        return items
    rev = (sort_dir == "desc")
    return sorted(items, key=lambda x: x.get(sort_by) or "", reverse=rev)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})



@app.route("/issues", methods=["GET"])
def list_issues():
    q = request.args.get("q", default=None, type=str)
    status = request.args.get("status", default=None, type=str)
    priority = request.args.get("priority", default=None, type=str)
    assignee = request.args.get("assignee", default=None, type=str)
    sort_by = request.args.get("sortBy", default=None, type=str)
    sort_dir = request.args.get("sortDir", default="asc", type=str)

    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
    except ValueError:
        page = 1
        page_size = 10

    items = ISSUES.copy()
    items = apply_search(items, q)
    items = apply_filters(items, status, priority, assignee)
    total = len(items)
    items = apply_sort(items, sort_by, sort_dir)

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
        return jsonify({"error": "Issue not found"}), 404
    return jsonify(item)


@app.route("/issues", methods=["POST"])
def create_issue():
    data = request.get_json(force=True)
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "open")
    priority = data.get("priority", "medium")
    assignee = data.get("assignee", None)
    new_item = {
        "id": next(_id_counter),
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "assignee": assignee,
        "createdAt": now_iso(),
        "updatedAt": now_iso()
    }
    ISSUES.append(new_item)
    return jsonify(new_item), 201



@app.route("/issues/<int:iid>", methods=["PUT"])
def update_issue(iid):
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "no data provided"}), 400
    item = next((x for x in ISSUES if x["id"] == iid), None)
    if not item:
        return jsonify({"error": "Issue not found"}), 404

    for k in ("title", "description", "status", "priority", "assignee"):
        if k in data:
            item[k] = data[k]
    item["updatedAt"] = now_iso()
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=True, port=5000)