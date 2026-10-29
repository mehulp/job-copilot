from copilot.storage import load_json

stories = load_json("data/stories.json")

for story in stories:
    themes = ", ".join(story["themes"])
    print(f"{story['id']}: {story['title']} ({themes})")