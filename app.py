#!/usr/bin/env python3
"""
ACEP ISO 27001 Web Audit Assistant
A Flask-based audit tool for ISO/IEC 27001:2022 compliance assessment
Created by A Chaitanya Eshwar Prasad
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'iso27001-audit-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('database', exist_ok=True)

# Database configuration
DATABASE = 'database/iso27001_audit.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ISO 27001 Controls table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Not Assessed',
            notes TEXT,
            assessed_by TEXT,
            assessed_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Evidence table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            uploaded_by TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (control_id) REFERENCES controls (control_id)
        )
    ''')
    
    # Risk register table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            likelihood INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
            impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
            risk_score INTEGER GENERATED ALWAYS AS (likelihood * impact) STORED,
            mitigation TEXT,
            owner TEXT,
            status TEXT DEFAULT 'Open',
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Create default admin user if not exists
    admin_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('acep',)).fetchone()
    if not admin_exists:
        password_hash = generate_password_hash('acep123')
        conn.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                    ('acep', password_hash, 'acep@chaitanyaeshwarprasad.com'))
        conn.commit()
    
    # Load ISO 27001:2022 controls if not exists
    controls_exist = conn.execute('SELECT COUNT(*) as count FROM controls').fetchone()
    if controls_exist['count'] == 0:
        load_iso27001_controls(conn)
    
    conn.close()

def load_iso27001_controls(conn):
    """Load ISO/IEC 27001:2022 Annex A controls into database"""
    controls = [
        # A.5 Organizational controls
        ('A.5.1', 'Policies for information security', 'Establish and maintain information security policy and topic-specific policies that define the organization\'s approach to information security', 'A.5 Organizational'),
        ('A.5.2', 'Information security roles and responsibilities', 'Define and allocate information security responsibilities to ensure clear accountability and ownership of security functions', 'A.5 Organizational'),
        ('A.5.3', 'Segregation of duties', 'Implement segregation of duties to prevent conflicts of interest and reduce the risk of fraud or error', 'A.5 Organizational'),
        ('A.5.4', 'Management responsibilities', 'Ensure management demonstrates leadership and commitment to information security through active support and resource allocation', 'A.5 Organizational'),
        ('A.5.5', 'Contact with authorities', 'Maintain appropriate contacts with relevant authorities to ensure compliance with legal and regulatory requirements', 'A.5 Organizational'),
        ('A.5.6', 'Contact with special interest groups', 'Engage with special interest groups and professional associations to stay informed about security trends and best practices', 'A.5 Organizational'),
        ('A.5.7', 'Threat intelligence', 'Collect and analyze information about information security threats to enhance security posture and incident response capabilities', 'A.5 Organizational'),
        ('A.5.8', 'Information security in project management', 'Integrate information security requirements into project management processes to ensure security is built-in from the start', 'A.5 Organizational'),
        ('A.5.9', 'Inventory of information and other associated assets', 'Maintain an accurate inventory of information assets and their associated systems, applications, and data stores', 'A.5 Organizational'),
        ('A.5.10', 'Acceptable use of information and other associated assets', 'Define and communicate rules for acceptable use of information assets to prevent misuse and ensure proper handling', 'A.5 Organizational'),
        ('A.5.11', 'Return of assets', 'Establish procedures for the secure return of assets when employment ends or access is no longer required', 'A.5 Organizational'),
        ('A.5.12', 'Classification of information', 'Implement information classification scheme to categorize data based on sensitivity and business impact', 'A.5 Organizational'),
        ('A.5.13', 'Labelling of information', 'Apply appropriate labels to information assets to indicate classification level and handling requirements', 'A.5 Organizational'),
        ('A.5.14', 'Information transfer', 'Establish secure procedures for transferring information between parties, including external organizations and third parties', 'A.5 Organizational'),
        ('A.5.15', 'Access control', 'Implement comprehensive access control policies and procedures to ensure authorized access to information assets', 'A.5 Organizational'),
        ('A.5.16', 'Identity management', 'Establish identity management processes to create, maintain, and revoke user identities throughout their lifecycle', 'A.5 Organizational'),
        ('A.5.17', 'Authentication information', 'Implement secure processes for managing authentication credentials, including password policies and multi-factor authentication', 'A.5 Organizational'),
        ('A.5.18', 'Access rights', 'Define and manage access rights to ensure users have appropriate permissions based on their roles and responsibilities', 'A.5 Organizational'),
        ('A.5.19', 'Information security in supplier relationships', 'Establish security requirements for supplier relationships to protect information shared with third parties', 'A.5 Organizational'),
        ('A.5.20', 'Addressing information security within supplier agreements', 'Include specific security requirements in supplier agreements to ensure contractual protection of information assets', 'A.5 Organizational'),
        ('A.5.21', 'Managing information security in the ICT supply chain', 'Implement security controls throughout the ICT supply chain to mitigate risks from suppliers and vendors', 'A.5 Organizational'),
        ('A.5.22', 'Monitoring, review and change management of supplier services', 'Continuously monitor and review supplier services to ensure ongoing compliance with security requirements', 'A.5 Organizational'),
        ('A.5.23', 'Information security for use of cloud services', 'Implement security controls for cloud services to protect data and ensure compliance with security policies', 'A.5 Organizational'),
        ('A.5.24', 'Information security incident management planning and preparation', 'Develop incident management plans and prepare response teams to effectively handle security incidents', 'A.5 Organizational'),
        ('A.5.25', 'Assessment and decision on information security events', 'Establish processes to assess security events and make decisions on incident classification and response', 'A.5 Organizational'),
        ('A.5.26', 'Response to information security incidents', 'Implement incident response procedures to contain, eradicate, and recover from security incidents', 'A.5 Organizational'),
        ('A.5.27', 'Learning from information security incidents', 'Analyze incidents to identify lessons learned and implement improvements to prevent future occurrences', 'A.5 Organizational'),
        ('A.5.28', 'Collection of evidence', 'Establish procedures for collecting and preserving evidence during security incidents for forensic analysis and legal proceedings', 'A.5 Organizational'),
        ('A.5.29', 'Information security during disruption', 'Maintain information security during business disruptions to ensure continuity of security operations', 'A.5 Organizational'),
        ('A.5.30', 'ICT readiness for business continuity', 'Ensure ICT systems are prepared to support business continuity requirements during disruptions', 'A.5 Organizational'),
        ('A.5.31', 'Legal, statutory, regulatory and contractual requirements', 'Identify and comply with applicable legal, regulatory, and contractual requirements related to information security', 'A.5 Organizational'),
        ('A.5.32', 'Intellectual property rights', 'Protect intellectual property rights and ensure compliance with copyright, patent, and trademark laws', 'A.5 Organizational'),
        ('A.5.33', 'Protection of records', 'Implement controls to protect important records from loss, destruction, and unauthorized access', 'A.5 Organizational'),
        ('A.5.34', 'Privacy and protection of personally identifiable information', 'Protect personally identifiable information (PII) in accordance with privacy laws and regulations', 'A.5 Organizational'),
        ('A.5.35', 'Independent review of information security', 'Conduct independent reviews of information security to ensure effectiveness and identify areas for improvement', 'A.5 Organizational'),
        ('A.5.36', 'Compliance with policies, rules and standards for information security', 'Ensure compliance with established information security policies, rules, and standards', 'A.5 Organizational'),
        ('A.5.37', 'Documented operating procedures', 'Document operating procedures to ensure consistent and secure execution of security processes', 'A.5 Organizational'),
        
        # A.6 People controls
        ('A.6.1', 'Screening', 'Conduct comprehensive background verification checks on all employment candidates to ensure trustworthiness and suitability for roles', 'A.6 People'),
        ('A.6.2', 'Terms and conditions of employment', 'Include information security responsibilities in employment terms and conditions to establish clear expectations', 'A.6 People'),
        ('A.6.3', 'Information security awareness, education and training', 'Provide ongoing security awareness, education, and training to ensure staff understand security policies and procedures', 'A.6 People'),
        ('A.6.4', 'Disciplinary process', 'Establish disciplinary procedures for security policy violations to enforce compliance and deter misconduct', 'A.6 People'),
        ('A.6.5', 'Responsibilities after termination or change of employment', 'Define security responsibilities that continue after employment ends to protect organizational assets', 'A.6 People'),
        ('A.6.6', 'Confidentiality or non-disclosure agreements', 'Require confidentiality agreements to protect sensitive information and establish legal obligations', 'A.6 People'),
        ('A.6.7', 'Remote working', 'Implement security controls for remote working to protect information accessed outside organizational premises', 'A.6 People'),
        ('A.6.8', 'Information security event reporting', 'Establish clear procedures for staff to report security events and incidents for timely response', 'A.6 People'),
        
        # A.7 Physical controls
        ('A.7.1', 'Physical security perimeters', 'Establish physical security perimeters to protect information processing facilities from unauthorized access', 'A.7 Physical'),
        ('A.7.2', 'Physical entry', 'Implement physical entry controls to restrict access to secure areas to authorized personnel only', 'A.7 Physical'),
        ('A.7.3', 'Protection against environmental threats', 'Protect information processing facilities against environmental threats such as fire, flood, and power failures', 'A.7 Physical'),
        ('A.7.4', 'Working in secure areas', 'Establish procedures for working in secure areas to maintain physical security controls', 'A.7 Physical'),
        ('A.7.5', 'Desk and screen', 'Implement clear desk and clear screen policies to prevent unauthorized access to information', 'A.7 Physical'),
        ('A.7.6', 'Protection of equipment', 'Protect equipment from environmental threats and unauthorized access to prevent damage or theft', 'A.7 Physical'),
        ('A.7.7', 'Secure disposal or reuse of equipment', 'Ensure secure disposal or reuse of equipment to prevent information leakage and unauthorized access', 'A.7 Physical'),
        ('A.7.8', 'Unattended user equipment', 'Implement controls for unattended user equipment to prevent unauthorized access and information exposure', 'A.7 Physical'),
        ('A.7.9', 'Clear desk and clear screen', 'Enforce clear desk and clear screen policies to protect sensitive information from unauthorized viewing', 'A.7 Physical'),
        ('A.7.10', 'Storage media', 'Implement secure storage media management to protect information from unauthorized access and damage', 'A.7 Physical'),
        ('A.7.11', 'Supporting utilities', 'Protect supporting utilities such as power, air conditioning, and telecommunications to ensure system availability', 'A.7 Physical'),
        ('A.7.12', 'Cabling security', 'Secure power and network cabling to prevent unauthorized access and interference with information systems', 'A.7 Physical'),
        ('A.7.13', 'Equipment maintenance', 'Establish secure equipment maintenance procedures to prevent unauthorized access and ensure system integrity', 'A.7 Physical'),
        ('A.7.14', 'Secure disposal or reuse of equipment', 'Implement secure disposal procedures for equipment to prevent information leakage and ensure environmental compliance', 'A.7 Physical'),
        
        # A.8 Technological controls
        ('A.8.1', 'User endpoint devices', 'Implement security controls for user endpoint devices to protect against threats and unauthorized access', 'A.8 Technological'),
        ('A.8.2', 'Privileged access rights', 'Control and monitor privileged access rights to prevent abuse and unauthorized system access', 'A.8 Technological'),
        ('A.8.3', 'Information access restriction', 'Restrict access to information systems and applications based on business requirements and user roles', 'A.8 Technological'),
        ('A.8.4', 'Access to source code', 'Control access to source code to prevent unauthorized modifications and protect intellectual property', 'A.8 Technological'),
        ('A.8.5', 'Secure authentication', 'Implement secure authentication mechanisms including multi-factor authentication and strong password policies', 'A.8 Technological'),
        ('A.8.6', 'Capacity management', 'Monitor and manage system capacity to ensure adequate performance and prevent service degradation', 'A.8 Technological'),
        ('A.8.7', 'Protection against malware', 'Implement anti-malware controls to detect, prevent, and remove malicious software', 'A.8 Technological'),
        ('A.8.8', 'Management of technical vulnerabilities', 'Establish vulnerability management processes to identify, assess, and remediate security weaknesses', 'A.8 Technological'),
        ('A.8.9', 'Configuration management', 'Implement configuration management to maintain secure system settings and prevent unauthorized changes', 'A.8 Technological'),
        ('A.8.10', 'Information deletion', 'Ensure secure deletion of information to prevent data recovery and unauthorized access', 'A.8 Technological'),
        ('A.8.11', 'Data masking', 'Implement data masking techniques to protect sensitive information during development and testing', 'A.8 Technological'),
        ('A.8.12', 'Data leakage prevention', 'Deploy data leakage prevention controls to monitor and prevent unauthorized data exfiltration', 'A.8 Technological'),
        ('A.8.13', 'Information backup', 'Implement regular backup procedures to ensure data availability and recovery capabilities', 'A.8 Technological'),
        ('A.8.14', 'Redundancy of information processing facilities', 'Implement redundant systems to ensure business continuity and minimize downtime', 'A.8 Technological'),
        ('A.8.15', 'Logging', 'Enable comprehensive logging of system activities for security monitoring and incident investigation', 'A.8 Technological'),
        ('A.8.16', 'Monitoring activities', 'Implement continuous monitoring of information systems to detect security events and anomalies', 'A.8 Technological'),
        ('A.8.17', 'Clock synchronisation', 'Synchronize system clocks to ensure accurate timestamps for security logs and audit trails', 'A.8 Technological'),
        ('A.8.18', 'Use of privileged utility programs', 'Control and monitor the use of privileged utility programs to prevent system abuse', 'A.8 Technological'),
        ('A.8.19', 'Installation of software on operational systems', 'Control software installation on operational systems to prevent unauthorized modifications', 'A.8 Technological'),
        ('A.8.20', 'Networks security management', 'Implement network security controls to protect against network-based attacks and unauthorized access', 'A.8 Technological'),
        ('A.8.21', 'Security of network services', 'Secure network services to prevent unauthorized access and ensure service availability', 'A.8 Technological'),
        ('A.8.22', 'Segregation of networks', 'Implement network segmentation to isolate systems and limit the impact of security incidents', 'A.8 Technological'),
        ('A.8.23', 'Web filtering', 'Deploy web filtering controls to prevent access to malicious websites and inappropriate content', 'A.8 Technological'),
        ('A.8.24', 'Use of cryptography', 'Implement cryptographic controls to protect data confidentiality, integrity, and authenticity', 'A.8 Technological'),
        ('A.8.25', 'Secure system development life cycle', 'Integrate security into the system development life cycle to build security into applications', 'A.8 Technological'),
        ('A.8.26', 'Application security requirements', 'Define security requirements for applications to ensure secure design and implementation', 'A.8 Technological'),
        ('A.8.27', 'Secure system architecture and engineering principles', 'Apply secure architecture and engineering principles to design robust and secure systems', 'A.8 Technological'),
        ('A.8.28', 'Secure coding', 'Implement secure coding practices to prevent common vulnerabilities and security weaknesses', 'A.8 Technological'),
        ('A.8.29', 'Security testing in development and acceptance', 'Conduct security testing during development and acceptance to identify and remediate vulnerabilities', 'A.8 Technological'),
        ('A.8.30', 'Outsourced development', 'Establish security requirements for outsourced development to ensure secure code delivery', 'A.8 Technological'),
        ('A.8.31', 'Separation of development, test and production environments', 'Separate development, test, and production environments to prevent unauthorized access and changes', 'A.8 Technological'),
        ('A.8.32', 'Change management', 'Implement change management processes to control system modifications and maintain security', 'A.8 Technological'),
        ('A.8.33', 'Test information', 'Protect test information to prevent exposure of sensitive data during testing activities', 'A.8 Technological'),
        ('A.8.34', 'Protection of information systems during audit testing', 'Protect information systems during audit testing to prevent disruption and maintain security', 'A.8 Technological')
    ]
    
    for control_id, title, description, category in controls:
        conn.execute('''
            INSERT OR IGNORE INTO controls (control_id, title, description, category)
            VALUES (?, ?, ?, ?)
        ''', (control_id, title, description, category))
    
    conn.commit()

# Authentication helper functions
def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with audit overview"""
    conn = get_db_connection()
    
    # Get control statistics
    total_controls = conn.execute('SELECT COUNT(*) as count FROM controls').fetchone()['count']
    compliant_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Compliant'").fetchone()['count']
    non_compliant_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Compliant'").fetchone()['count']
    not_applicable_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Applicable'").fetchone()['count']
    not_assessed_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Assessed'").fetchone()['count']
    
    # Get risk statistics
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    high_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 15').fetchone()['count']
    medium_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 8 AND risk_score < 15').fetchone()['count']
    low_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score < 8').fetchone()['count']
    
    # Get recent activity
    recent_controls = conn.execute('''
        SELECT control_id, title, status, assessed_at 
        FROM controls 
        WHERE assessed_at IS NOT NULL 
        ORDER BY assessed_at DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    # Calculate compliance percentage
    assessed_controls = total_controls - not_assessed_controls
    compliance_percentage = (compliant_controls / assessed_controls * 100) if assessed_controls > 0 else 0
    
    return render_template('dashboard.html',
                         total_controls=total_controls,
                         compliant_controls=compliant_controls,
                         non_compliant_controls=non_compliant_controls,
                         not_applicable_controls=not_applicable_controls,
                         not_assessed_controls=not_assessed_controls,
                         compliance_percentage=round(compliance_percentage, 1),
                         total_risks=total_risks,
                         high_risks=high_risks,
                         medium_risks=medium_risks,
                         low_risks=low_risks,
                         recent_controls=recent_controls)

@app.route('/audit-checklist')
@login_required
def audit_checklist():
    """Audit checklist page with all controls"""
    conn = get_db_connection()
    
    # Get category filter
    category_filter = request.args.get('category', '')
    
    # Build query based on filter
    if category_filter:
        controls = conn.execute('''
            SELECT * FROM controls 
            WHERE category = ? 
            ORDER BY control_id
        ''', (category_filter,)).fetchall()
    else:
        controls = conn.execute('SELECT * FROM controls ORDER BY control_id').fetchall()
    
    # Get all categories for filter dropdown
    categories = conn.execute('''
        SELECT DISTINCT category FROM controls ORDER BY category
    ''').fetchall()
    
    conn.close()
    
    return render_template('audit_checklist.html', 
                         controls=controls, 
                         categories=categories,
                         current_category=category_filter)

@app.route('/audit-checklist/update/<control_id>', methods=['POST'])
@login_required
def update_control(control_id):
    """Update control status and notes"""
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE controls 
        SET status = ?, notes = ?, assessed_by = ?, assessed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE control_id = ?
    ''', (status, notes, session['username'], control_id))
    conn.commit()
    conn.close()
    
    # Handle AJAX requests
    if request.headers.get('X-Auto-Save'):
        return {'success': True}
    
    flash(f'Control {control_id} updated successfully!', 'success')
    return redirect(url_for('audit_checklist'))

@app.route('/evidence')
@login_required
def evidence():
    """Evidence management page"""
    conn = get_db_connection()
    
    # Get all evidence with control information
    evidence_list = conn.execute('''
        SELECT e.*, c.title as control_title
        FROM evidence e
        LEFT JOIN controls c ON e.control_id = c.control_id
        ORDER BY e.uploaded_at DESC
    ''').fetchall()
    
    # Get all controls for the upload form
    controls = conn.execute('SELECT control_id, title FROM controls ORDER BY control_id').fetchall()
    
    conn.close()
    
    return render_template('evidence.html', evidence_list=evidence_list, controls=controls)

@app.route('/evidence/upload', methods=['POST'])
@login_required
def upload_evidence():
    """Upload evidence file"""
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    file = request.files['file']
    control_id = request.form.get('control_id')
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    if file and control_id:
        # Secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Store in database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO evidence (control_id, filename, original_filename, file_path, file_size, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (control_id, filename, file.filename, file_path, 
              os.path.getsize(file_path), session['username']))
        conn.commit()
        conn.close()
        
        flash(f'Evidence uploaded successfully for control {control_id}!', 'success')
    else:
        flash('Invalid file or control selection!', 'error')
    
    return redirect(url_for('evidence'))

@app.route('/evidence/download/<int:evidence_id>')
@login_required
def download_evidence(evidence_id):
    """Download evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    conn.close()
    
    if evidence and os.path.exists(evidence['file_path']):
        return send_file(evidence['file_path'], 
                        as_attachment=True, 
                        download_name=evidence['original_filename'])
    else:
        flash('File not found!', 'error')
        return redirect(url_for('evidence'))

@app.route('/risk-register')
@login_required
def risk_register():
    """Risk register page"""
    conn = get_db_connection()
    
    risks = conn.execute('''
        SELECT * FROM risks 
        ORDER BY risk_score DESC, created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('risk_register.html', risks=risks)

@app.route('/risk-register/add', methods=['POST'])
@login_required
def add_risk():
    """Add new risk to register"""
    title = request.form.get('title')
    description = request.form.get('description', '')
    likelihood = int(request.form.get('likelihood'))
    impact = int(request.form.get('impact'))
    mitigation = request.form.get('mitigation', '')
    owner = request.form.get('owner', '')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO risks (title, description, likelihood, impact, mitigation, owner, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, likelihood, impact, mitigation, owner, session['username']))
    conn.commit()
    conn.close()
    
    flash('Risk added successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/risk-register/update/<int:risk_id>', methods=['POST'])
@login_required
def update_risk(risk_id):
    """Update existing risk"""
    title = request.form.get('title')
    description = request.form.get('description', '')
    likelihood = int(request.form.get('likelihood'))
    impact = int(request.form.get('impact'))
    mitigation = request.form.get('mitigation', '')
    owner = request.form.get('owner', '')
    status = request.form.get('status', 'Open')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE risks 
        SET title = ?, description = ?, likelihood = ?, impact = ?, 
            mitigation = ?, owner = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (title, description, likelihood, impact, mitigation, owner, status, risk_id))
    conn.commit()
    conn.close()
    
    flash('Risk updated successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')

@app.route('/reports/risk')
@login_required
def risk_report():
    """Generate risk assessment report"""
    conn = get_db_connection()
    risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
    conn.close()
    
    return render_template('risk_report.html', risks=risks, generated_at=datetime.now(), generated_by=session['username'])

@app.route('/reports/evidence')
@login_required
def evidence_report():
    """Generate evidence management report"""
    conn = get_db_connection()
    evidence = conn.execute('''
        SELECT e.*, c.title as control_title 
        FROM evidence e 
        LEFT JOIN controls c ON e.control_id = c.control_id 
        ORDER BY e.uploaded_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('evidence_report.html', evidence=evidence, generated_at=datetime.now(), generated_by=session['username'])

@app.route('/reports/export/html')
@login_required
def export_html():
    """Export audit report as HTML"""
    return generate_report()

@app.route('/reports/export/csv')
@login_required
def export_csv():
    """Export audit report as CSV"""
    import csv
    from io import StringIO, BytesIO
    
    conn = get_db_connection()
    
    # Get all data for the report
    controls = conn.execute('SELECT * FROM controls ORDER BY control_id').fetchall()
    risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
    
    conn.close()
    
    # Create CSV content in memory
    string_buffer = StringIO()
    writer = csv.writer(string_buffer)
    
    # Write headers
    writer.writerow(['ISO 27001:2022 Audit Report'])
    writer.writerow(['Generated at:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['Generated by:', session['username']])
    writer.writerow([])
    
    # Write controls
    writer.writerow(['Controls Assessment'])
    writer.writerow(['Control ID', 'Title', 'Status', 'Notes', 'Assessed By', 'Assessed At'])
    for control in controls:
        writer.writerow([
            control['control_id'],
            control['title'],
            control['status'],
            control['notes'] or '',
            control['assessed_by'] or '',
            control['assessed_at'] or ''
        ])
    
    writer.writerow([])
    
    # Write risks
    writer.writerow(['Risk Register'])
    writer.writerow(['Title', 'Description', 'Likelihood', 'Impact', 'Risk Score', 'Status', 'Owner'])
    for risk in risks:
        writer.writerow([
            risk['title'],
            risk['description'] or '',
            risk['likelihood'],
            risk['impact'],
            risk['risk_score'],
            risk['status'],
            risk['owner'] or ''
        ])
    
    # Convert to bytes for file download
    csv_bytes = string_buffer.getvalue().encode('utf-8')
    byte_buffer = BytesIO(csv_bytes)
    byte_buffer.seek(0)
    
    return send_file(
        byte_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'iso27001_audit_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/reports/export/json')
@login_required
def export_json():
    """Export audit report as JSON"""
    conn = get_db_connection()
    
    # Get all data for the report
    controls = conn.execute('SELECT * FROM controls ORDER BY control_id').fetchall()
    risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
    evidence_count = conn.execute('SELECT COUNT(*) as count FROM evidence').fetchone()['count']
    
    # Calculate statistics
    total_controls = len(controls)
    compliant_controls = len([c for c in controls if c['status'] == 'Compliant'])
    non_compliant_controls = len([c for c in controls if c['status'] == 'Not Compliant'])
    not_applicable_controls = len([c for c in controls if c['status'] == 'Not Applicable'])
    not_assessed_controls = len([c for c in controls if c['status'] == 'Not Assessed'])
    
    conn.close()
    
    # Generate report data
    report_data = {
        'generated_at': datetime.now().isoformat(),
        'generated_by': session['username'],
        'controls': [dict(control) for control in controls],
        'risks': [dict(risk) for risk in risks],
        'evidence_count': evidence_count,
        'total_controls': total_controls,
        'compliant_controls': compliant_controls,
        'non_compliant_controls': non_compliant_controls,
        'not_applicable_controls': not_applicable_controls,
        'not_assessed_controls': not_assessed_controls,
        'compliance_percentage': round((compliant_controls / (total_controls - not_assessed_controls) * 100) if total_controls > not_assessed_controls else 0, 1)
    }
    
    return jsonify(report_data)

@app.route('/reports/generate')
@login_required
def generate_report():
    """Generate and download audit report"""
    conn = get_db_connection()
    
    # Get all data for the report
    controls = conn.execute('SELECT * FROM controls ORDER BY control_id').fetchall()
    risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
    evidence_count = conn.execute('SELECT COUNT(*) as count FROM evidence').fetchone()['count']
    
    # Calculate statistics
    total_controls = len(controls)
    compliant_controls = len([c for c in controls if c['status'] == 'Compliant'])
    non_compliant_controls = len([c for c in controls if c['status'] == 'Not Compliant'])
    not_applicable_controls = len([c for c in controls if c['status'] == 'Not Applicable'])
    not_assessed_controls = len([c for c in controls if c['status'] == 'Not Assessed'])
    
    conn.close()
    
    # Generate report HTML
    report_data = {
        'generated_at': datetime.now(),
        'generated_by': session['username'],
        'controls': controls,
        'risks': risks,
        'evidence_count': evidence_count,
        'total_controls': total_controls,
        'compliant_controls': compliant_controls,
        'non_compliant_controls': non_compliant_controls,
        'not_applicable_controls': not_applicable_controls,
        'not_assessed_controls': not_assessed_controls,
        'compliance_percentage': round((compliant_controls / (total_controls - not_assessed_controls) * 100) if total_controls > not_assessed_controls else 0, 1)
    }
    
    return render_template('report.html', **report_data)

@app.route('/api/dashboard-stats')
@login_required
def api_dashboard_stats():
    """API endpoint for dashboard statistics"""
    conn = get_db_connection()
    
    # Get control statistics
    total_controls = conn.execute('SELECT COUNT(*) as count FROM controls').fetchone()['count']
    compliant_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Compliant'").fetchone()['count']
    non_compliant_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Compliant'").fetchone()['count']
    not_applicable_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Applicable'").fetchone()['count']
    not_assessed_controls = conn.execute("SELECT COUNT(*) as count FROM controls WHERE status = 'Not Assessed'").fetchone()['count']
    
    # Get risk statistics
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    
    conn.close()
    
    # Calculate compliance percentage
    assessed_controls = total_controls - not_assessed_controls
    compliance_percentage = round((compliant_controls / assessed_controls * 100) if assessed_controls > 0 else 0, 1)
    
    return jsonify({
        'total_controls': total_controls,
        'compliant_controls': compliant_controls,
        'non_compliant_controls': non_compliant_controls,
        'not_applicable_controls': not_applicable_controls,
        'not_assessed_controls': not_assessed_controls,
        'compliance_percentage': compliance_percentage,
        'total_risks': total_risks
    })

@app.route('/evidence/delete/<int:evidence_id>', methods=['DELETE'])
@login_required
def delete_evidence(evidence_id):
    """Delete evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    
    if evidence:
        # Delete file from filesystem
        if os.path.exists(evidence['file_path']):
            os.remove(evidence['file_path'])
        
        # Delete from database
        conn.execute('DELETE FROM evidence WHERE id = ?', (evidence_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Evidence deleted successfully'})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'Evidence not found'}), 404

# Template helper functions
@app.template_filter('format_file_size')
def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

@app.template_filter('get_file_icon')
def get_file_icon(filename):
    """Get Bootstrap icon class based on file extension"""
    if not filename:
        return 'bi-file'
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    icon_map = {
        'pdf': 'bi-file-pdf',
        'doc': 'bi-file-word',
        'docx': 'bi-file-word',
        'xls': 'bi-file-excel',
        'xlsx': 'bi-file-excel',
        'ppt': 'bi-file-ppt',
        'pptx': 'bi-file-ppt',
        'txt': 'bi-file-text',
        'jpg': 'bi-file-image',
        'jpeg': 'bi-file-image',
        'png': 'bi-file-image',
        'gif': 'bi-file-image',
        'zip': 'bi-file-zip',
        'rar': 'bi-file-zip',
        '7z': 'bi-file-zip'
    }
    
    return icon_map.get(ext, 'bi-file')

@app.template_global()
def moment():
    """Template global for current datetime"""
    return datetime.now()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_database()
    print("ACEP ISO 27001 Audit Tool starting...")
    print("Created by A Chaitanya Eshwar Prasad")
    print("Access the application at: http://localhost:5000")
    print("Default login: acep / acep123")
    app.run(debug=True, host='0.0.0.0', port=5000)
