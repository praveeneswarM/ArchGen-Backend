from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RequirementInput(BaseModel):
    expected_users: str = Field(..., example="100,000 monthly")
    monthly_budget: str = Field(..., example="500")
    cloud_provider: str = Field("azure", example="azure")
    app_description: str = Field(..., example="A global OTT video streaming platform requiring high throughput and low latency.")
    additional_notes: Optional[str] = Field(None, example="Needs highly secure administrative controls.")

class NodePosition(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    label: str
    status: Optional[str] = "active"
    cost: Optional[str] = None
    typeSubText: Optional[str] = None

class NodeSchema(BaseModel):
    id: str
    type: str
    data: NodeData
    position: NodePosition

class EdgeSchema(BaseModel):
    id: str
    source: str
    target: str
    animated: Optional[bool] = False

class ServiceSchema(BaseModel):
    name: str
    category: str
    description: str

class CostBreakdownItem(BaseModel):
    service: str
    cost: float
    reason: str

class SecurityFinding(BaseModel):
    severity: str
    description: str
    remediation: str

class ComplianceCheck(BaseModel):
    standard: str
    status: str
    notes: str

class ArchitectureResponse(BaseModel):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]
    services: List[ServiceSchema]
    cloud_provider: str
    active_provider: Optional[str] = None
    active_model: Optional[str] = None
    fallback_trigger: Optional[str] = None
    cost_estimate: float
    cost_breakdown: List[CostBreakdownItem]
    optimization_recommendations: List[str]
    complexity_score: int
    operational_overhead_score: int
    overengineered: bool
    warnings: List[str]
    security_score: int
    security_findings: List[SecurityFinding]
    compliance_checks: List[ComplianceCheck]
    explanation: str
    alternatives_considered: str
    justification_for_choices: str
    terraform_modules: List[str]
    execution_time_ms: Optional[int] = None

class TerraformRequest(BaseModel):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]
    services: List[ServiceSchema]
    cloud_provider: str

class TerraformResponse(BaseModel):
    main_tf: str
    variables_tf: str
    outputs_tf: str
    terraform_tfvars: str
    instructions: str

class AiAssistRequest(BaseModel):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]
    services: List[ServiceSchema]
    action: str = Field(..., example="optimize_security")
