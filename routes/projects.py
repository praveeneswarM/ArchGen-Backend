from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from bson import ObjectId
from utils.db import get_database
from routes.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

class ProjectSaveInput(BaseModel):
    id: Optional[str] = None  # None for new project, string ID to overwrite
    name: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    services: List[Dict[str, Any]]
    cloud_provider: str
    cost_estimate: float

@router.post("")
async def save_project(input_data: ProjectSaveInput, current_user: dict = Depends(get_current_user)):
    db = get_database()
    if db is None:
        return {"status": "success", "message": "Mock save successful."}
        
    project_doc = {
        "username": current_user["username"],
        "name": input_data.name,
        "nodes": input_data.nodes,
        "edges": input_data.edges,
        "services": input_data.services,
        "cloud_provider": input_data.cloud_provider,
        "cost_estimate": input_data.cost_estimate
    }
    
    if input_data.id:
        try:
            object_id = ObjectId(input_data.id)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid project identifier formatting.")

        result = await db["projects"].update_one(
            {"_id": object_id, "username": current_user["username"]},
            {"$set": project_doc}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Project not found or unauthorized.")
        return {"status": "success", "id": input_data.id, "message": "Project updated successfully."}
    else:
        result = await db["projects"].insert_one(project_doc)
        return {"status": "success", "id": str(result.inserted_id), "message": "Project saved successfully."}

@router.get("")
async def list_projects(current_user: dict = Depends(get_current_user)):
    db = get_database()
    if db is None:
        # Fallback empty array
        return []
        
    cursor = db["projects"].find({"username": current_user["username"]})
    projects = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        projects.append(doc)
    return projects

@router.get("/{project_id}")
async def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=404, detail="Mock database active. Project not found.")
        
    try:
        project = await db["projects"].find_one({"_id": ObjectId(project_id), "username": current_user["username"]})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")
        project["id"] = str(project["_id"])
        del project["_id"]
        return project
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed project identifier.")

@router.delete("/{project_id}")
async def delete_project(project_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    if db is None:
        return {"status": "success", "message": "Mock delete successful."}
        
    try:
        result = await db["projects"].delete_one({"_id": ObjectId(project_id), "username": current_user["username"]})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found or unauthorized.")
        return {"status": "success", "message": "Project deleted successfully."}
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed project identifier.")
