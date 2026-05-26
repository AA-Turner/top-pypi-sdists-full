import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

BACKEND_MOCKS = {
    "fastapi_postgres": """
Output for FastAPI Postgres:
FILE: models.py
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AdCampaign(Base):
    __tablename__ = "ad_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    budget = Column(Integer)
    is_active = Column(Boolean, default=True)
```
FILE: main.py
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import AdCampaign

app = FastAPI(title="Ad Platform")

@app.post("/campaigns/")
def create_campaign(name: str, budget: int):
    # Valid complete route, no placeholders
    return {"status": "created", "name": name, "budget": budget}
```
""",
    "nestjs_typescript": """
Output for NestJS App:
FILE: campaign.controller.ts
```typescript
import { Controller, Post, Body, Get } from '@nestjs/common';

@Controller('campaigns')
export class CampaignController {
    private campaigns = [];

    @Post()
    create(@Body() dto: { name: string; budget: number }) {
        const campaign = { id: this.campaigns.length + 1, ...dto };
        this.campaigns.push(campaign);
        return campaign;
    }

    @Get()
    findAll() {
        return this.campaigns;
    }
}
```
""",
    "springboot_java": """
Output for Spring Boot App:
FILE: CampaignController.java
```java
package com.sage.adplatform.controller;

import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/campaigns")
public class CampaignController {
    private final List<String> campaigns = new ArrayList<>();

    @PostMapping
    public String createCampaign(@RequestBody String name) {
        campaigns.add(name);
        return "Campaign created: " + name;
    }

    @GetMapping
    public List<String> getAllCampaigns() {
        return campaigns;
    }
}
```
""",
    "go_gin": """
Output for Go/Gin App:
FILE: main.go
```go
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()
	r.POST("/campaigns", func(c *gin.Context) {
		var json struct {
			Name   string `json:"name" binding:"required"`
			Budget int    `json:"budget" binding:"required"`
		}
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, gin.H{"status": "created", "name": json.Name})
	})
	r.Run()
}
```
""",
    "rust_axum": """
Output for Rust/Axum App:
FILE: main.rs
```rust
use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;

#[derive(Deserialize, Serialize)]
struct CreateCampaign {
    name: String,
    budget: u32,
}

async fn create_campaign(Json(payload): Json<CreateCampaign>) -> Json<CreateCampaign> {
    Json(payload)
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/campaigns", post(create_campaign));
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```
"""
}

@pytest.mark.parametrize("framework", ["fastapi_postgres", "nestjs_typescript", "springboot_java", "go_gin", "rust_axum"])
def test_backend_framework_generation(framework):
    """Verify backend framework tasks are written and validate perfectly."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    mock_output = BACKEND_MOCKS[framework]

    with patch("sage.main._prepare_model_for_use") as mock_prep, \
         patch("sage.main._build_router") as mock_router:
         
        mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
        mock_router_inst = MagicMock()
        mock_router_inst.stream.return_value = [mock_output]
        mock_router.return_value = mock_router_inst
        
        with runner.isolated_filesystem():
            result = runner.invoke(sage_app, ["ask", prompt, "--raw", "--agent"])
            assert result.exit_code == 0, f"Task failed: {result.output}"
            
            generated_files = [
                f for f in Path(".").glob("**/*")
                if f.is_file() and not any(part.startswith(".") or part in ("venv", "__pycache__") for part in f.parts) and f.suffix != ".pyc"
            ]
            assert len(generated_files) > 0, "No files written"
            
            for f in generated_files:
                content = f.read_text(encoding="utf-8")
                val_res = validate_content(str(f), content)
                assert val_res.ok, f"File {f} contains placeholders: {val_res.reason}"
