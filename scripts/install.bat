@echo off
REM short-story-hit 一键安装脚本（Windows）
REM 将 skill\short-story-hit 复制到常见 Agent 平台的 skills 目录。
setlocal
set "SCRIPT_DIR=%~dp0"
set "SKILL_SRC=%SCRIPT_DIR%skill\short-story-hit"

echo == short-story-hit 安装 ==
echo 技能源目录: %SKILL_SRC%
echo.

if exist "%USERPROFILE%\.claude\skills" (
  xcopy /E /I /Y "%SKILL_SRC%" "%USERPROFILE%\.claude\skills\short-story-hit" >nul
  echo [Claude Code] 已安装到 %USERPROFILE%\.claude\skills\short-story-hit
)

if exist "%USERPROFILE%\.cursor\skills" (
  xcopy /E /I /Y "%SKILL_SRC%" "%USERPROFILE%\.cursor\skills\short-story-hit" >nul
  echo [Cursor] 已安装到 %USERPROFILE%\.cursor\skills\short-story-hit
)

if exist "%USERPROFILE%\.openclaw\skills" (
  xcopy /E /I /Y "%SKILL_SRC%" "%USERPROFILE%\.openclaw\skills\short-story-hit" >nul
  echo [OpenClaw] 已安装到 %USERPROFILE%\.openclaw\skills\short-story-hit
)

echo.
echo 完成。未检测到的平台目录已跳过。
echo 提示：SkillHub 用户可手动上传 skill\short-story-hit\ 目录（SKILL.md + references\ + scripts\）。
pause
