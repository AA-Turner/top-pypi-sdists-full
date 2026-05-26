import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

GAME_MOCKS = {
    "unity_csharp": """
Output for Unity C#:
FILE: PlayerController.cs
```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed = 5.0f;
    private Rigidbody2D rb;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        float moveHorizontal = Input.GetAxis("Horizontal");
        float moveVertical = Input.GetAxis("Vertical");
        Vector2 movement = new Vector2(moveHorizontal, moveVertical);
        rb.velocity = movement * speed;
    }
}
```
""",
    "unreal_cpp": """
Output for Unreal C++:
FILE: MyCharacter.cpp
```cpp
#include "MyCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"

AMyCharacter::AMyCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    MoveSpeed = 600.f;
}

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    PlayerInputComponent->BindAxis("MoveForward", this, &AMyCharacter::MoveForward);
}

void AMyCharacter::MoveForward(float Value)
{
    if ((Controller != nullptr) && (Value != 0.0f))
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
        AddInputVector(Direction * Value * MoveSpeed);
    }
}
```
""",
    "godot_gdscript": """
Output for Godot GDScript:
FILE: player.gd
```gdscript
extends CharacterBody2D

@export var speed: float = 200.0

func _physics_process(delta: float) -> void:
	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	velocity = direction * speed
	move_and_slide()
```
""",
    "html5_canvas": """
Output for HTML5 Canvas:
FILE: game.js
```javascript
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let player = { x: 50, y: 50, size: 20, speed: 5 };

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#3b82f6";
    ctx.fillRect(player.x, player.y, player.size, player.size);
}

function update() {
    // Basic motion code
    draw();
    requestAnimationFrame(update);
}
update();
```
"""
}

@pytest.mark.parametrize("platform", ["unity_csharp", "unreal_cpp", "godot_gdscript", "html5_canvas"])
def test_video_game_platform_generation(platform):
    """Verify video game platform tasks are written and validate perfectly."""
    prompt = f"Implement a complete {platform} video game player movement script."
    mock_output = GAME_MOCKS[platform]

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
