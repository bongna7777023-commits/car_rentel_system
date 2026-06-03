# =====================================================
# DEPLOYMENT HELPER - Run this on YOUR local machine
# =====================================================

Write-Host "=== Step 1: Copy scripts to servers ===" -ForegroundColor Cyan

Write-Host "Copying DB script to dbms..." -ForegroundColor Yellow
scp .\deploy_db.sh pnc@dbms:~/deploy_db.sh

Write-Host "Copying App script to VANNA-web..." -ForegroundColor Yellow
scp .\deploy_app.sh pnc@VANNA-web:~/deploy_app.sh

Write-Host ""
Write-Host "=== Step 2: Run DB setup ===" -ForegroundColor Cyan
Write-Host "Open a new terminal and run:" -ForegroundColor Green
Write-Host "  ssh pnc@dbms 'bash ~/deploy_db.sh'" -ForegroundColor White

Write-Host ""
Write-Host "=== Step 3: Run App setup ===" -ForegroundColor Cyan
Write-Host "Open a new terminal and run:" -ForegroundColor Green
Write-Host "  ssh pnc@VANNA-web 'sudo bash ~/deploy_app.sh'" -ForegroundColor White

Write-Host ""
Write-Host "=== Step 4: Verify ===" -ForegroundColor Cyan
Write-Host "Open http://VANNA-web in your browser" -ForegroundColor Green
Write-Host "Admin: http://VANNA-web/admin/login (admin@luxedrive.com / AdminLuxe2024!)" -ForegroundColor Green
