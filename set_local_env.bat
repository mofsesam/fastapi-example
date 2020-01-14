@echo off
set DOCKER_USER=mofsesam
set GIT_USER=mofsesam
for /f "delims=" %%A in ('git rev-parse --abbrev-ref HEAD') do set "GIT_BRANCH=%%A"
REM for /f "delims=" %%A in ('keyring get Test_PW %USER%') do set "PW=%%A"
set DOCKER_TAG=%GIT_BRANCH%