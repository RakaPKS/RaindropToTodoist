from todoist_api_python.api import TodoistAPI
import constants

api = TodoistAPI(constants.TODOISTAUTH)

# Returns the ID of the project to store the bookmarks in
def getProjectID():
    try:
        projects = api.get_projects()
        return next((project.id for project in projects if constants.PROJECTNAME in project.name), None)
    except Exception as error:
        print(error)


# Returns the IDs of the sections to organize the bookmarks
def getSectionIDs(project_id):
    try:
        sections = api.get_sections(project_id=project_id)
        article_section_id = next(
            (section.id for section in sections if "Articles" in section.name), None)
        video_section_id = next(
            (section.id for section in sections if "Videos" in section.name), None)
        return article_section_id, video_section_id
    except Exception as error:
        print(error)

# Creates the tasks in Todoist
def createTasks(bookmarks):
    project_id = getProjectID()
    article_section_id, video_section_id = getSectionIDs(project_id)
    if project_id:
        try:
            for bookmark in bookmarks:
                if bookmark['type'] == "article" or bookmark['type'] == "link":
                    section_id = article_section_id
                elif bookmark['type'] == "video":
                    section_id = video_section_id
                else:
                    section_id = None
                api.add_task(content=bookmark['link'], project_id=project_id,
                             description=bookmark['title'] + "\n" + bookmark['excerpt'], section_id=section_id)
            return True
        except Exception as error:
            print(error)
    else:
        print("Project not found")
    return False
