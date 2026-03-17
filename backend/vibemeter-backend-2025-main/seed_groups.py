from app.utils.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""INSERT INTO focus_groups (focus_group_id, name, description, created_at) VALUES 
        ('GRP001', 'Consistently Dissatisfied', 'Employees with consistently low vibe scores', NOW()),
        ('GRP002', 'Volatile but Generally Happy', 'Employees with fluctuating but mostly positive scores', NOW()),
        ('GRP003', 'Inconsistent Satisfaction', 'Employees with inconsistent satisfaction patterns', NOW())
    ON CONFLICT DO NOTHING"""))
    
    result = conn.execute(text('SELECT employee_id FROM "user" LIMIT 30'))
    emps = [r[0] for r in result]
    
    for emp in emps[:5]:
        conn.execute(text("INSERT INTO user_group_association (employee_id, focus_group_id) VALUES (:emp, 'GRP001') ON CONFLICT DO NOTHING"), {'emp': emp})
    for emp in emps[5:15]:
        conn.execute(text("INSERT INTO user_group_association (employee_id, focus_group_id) VALUES (:emp, 'GRP002') ON CONFLICT DO NOTHING"), {'emp': emp})
    for emp in emps[15:30]:
        conn.execute(text("INSERT INTO user_group_association (employee_id, focus_group_id) VALUES (:emp, 'GRP003') ON CONFLICT DO NOTHING"), {'emp': emp})
    
    conn.commit()
    print('Focus groups created and employees assigned!')