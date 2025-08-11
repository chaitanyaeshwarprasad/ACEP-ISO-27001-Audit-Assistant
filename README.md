# 🛡️ ACEP ISO 27001 Audit Assistant

<div align="center">

![ACEP ISO 27001](https://img.shields.io/badge/ACEP-ISO%2027001%20Audit%20Assistant-blue?style=for-the-badge&logo=shield-check&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-red?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple?style=for-the-badge&logo=bootstrap&logoColor=white)

**Professional Information Security Management System Assessment Tool**

*Created by A Chaitanya Eshwar Prasad*  
*Built for security professionals, by security professionals.*

[![Website](https://img.shields.io/badge/🌐_Website-chaitanyaeshwarprasad.com-blue?style=for-the-badge&logo=globe&logoColor=white)](https://chaitanyaeshwarprasad.com)
[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chaitanya-eshwar-prasad)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/chaitanyaeshwarprasad)

</div>

---

## 🚀 **Quick Setup**

### **Option 1: Clone and Run (Recommended)**
```bash
# Clone the repository
git clone https://github.com/chaitanyaeshwarprasad/ACEP-ISO-27001-Audit-Assistant.git
cd ACEP-ISO-27001-Audit-Assistant

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### **Option 2: Download and Setup**
```bash
# Download ZIP from GitHub
# Extract and navigate to folder
cd ACEP-ISO-27001-Audit-Assistant

# Install Python dependencies
pip install -r requirements.txt

# Launch the application
python app.py
```

### **Access the Application**
- **URL:** http://localhost:5000
- **Default Credentials:** Check the application setup

### **System Requirements**
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 100MB free space
- **Browser:** Modern browser with JavaScript enabled

### **What You'll Get**
- 🎯 **Complete ISO 27001:2022 Control Coverage** (93 controls)
- 📊 **Real-time Dashboard** with compliance tracking
- 📎 **Evidence Management** system for file uploads
- ⚠️ **Risk Register** with automatic severity calculation
- 📄 **Professional Reports** in HTML format
- 🔐 **Secure Authentication** system
- 📱 **Responsive Design** for all devices

---

---

## 📋 **Table of Contents**

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Installation](#️-installation)
- [📱 Usage Guide](#-usage-guide)
- [🏗️ Architecture](#️-architecture)
- [🎨 UI/UX Features](#-uiux-features)
- [🔧 Technical Details](#-technical-details)
- [📊 Database Schema](#-database-schema)
- [🌐 API Endpoints](#-api-endpoints)
- [📁 Project Structure](#-project-structure)
- [🔒 Security Features](#-security-features)
- [📱 Responsive Design](#-responsive-design)
- [🚀 Performance Optimizations](#-performance-optimizations)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Creator](#-creator)

---

## 🎯 **Overview**

The **ACEP ISO 27001 Audit Assistant** is a comprehensive, web-based tool designed to streamline and enhance ISO/IEC 27001:2022 compliance assessments. Built with modern technologies and a focus on user experience, it provides auditors and compliance professionals with an intuitive interface to manage their information security management system (ISMS) audits.

### **Key Benefits**
- ✅ **Streamlined Auditing**: Complete ISO 27001:2022 Annex A control coverage
- ✅ **Professional Interface**: Modern tech gradient theme with glass-morphism design
- ✅ **Evidence Management**: Comprehensive file upload and association system
- ✅ **Risk Assessment**: Built-in risk register with severity calculations
- ✅ **Report Generation**: Automated HTML report creation
- ✅ **Real-time Progress**: Live dashboard with compliance tracking

---

## ✨ **Features**

### 🔐 **Authentication & Security**
- **Secure Login System**: User authentication with session management
- **Role-based Access**: Configurable user permissions
- **Session Security**: Secure session handling and timeout

### 📊 **Dashboard & Analytics**
- **Real-time Metrics**: Live compliance statistics and progress tracking
- **Visual Progress**: Interactive charts and progress indicators
- **Quick Actions**: Fast access to common audit tasks

### 📋 **Audit Management**
- **Complete Control Coverage**: All 93 ISO 27001:2022 Annex A controls
- **Status Tracking**: Compliant, Non-Compliant, Not Applicable, Not Assessed
- **Notes & Comments**: Detailed documentation for each control
- **Bulk Operations**: Efficient batch updates and management

### 📎 **Evidence Management**
- **File Uploads**: Support for PDF, DOCX, JPG, PNG, and more
- **Control Association**: Link evidence to specific controls
- **Metadata Tracking**: File information, upload dates, and descriptions
- **Search & Filter**: Quick evidence retrieval and organization

### ⚠️ **Risk Register**
- **Risk Assessment**: Likelihood and impact scoring (1-5 scale)
- **Severity Calculation**: Automatic risk level determination
- **Mitigation Planning**: Risk response and control measures
- **Trend Analysis**: Risk evolution over time

### 📄 **Reporting System**
- **HTML Reports**: Professional, printable audit reports
- **Customizable Content**: Include/exclude sections as needed
- **Export Options**: Download and share capabilities
- **Audit Trail**: Complete history of changes and assessments

---

## 🚀 **Quick Start**

### **Prerequisites**
- **Operating System**: Kali Linux (Debian-based)
- **Python**: 3.8 or higher
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

### **One-Command Setup**
```bash
# Download and run the automated setup
chmod +x acep_iso_auto_setup.sh
./acep_iso_auto_setup.sh
```

### **Access Application**
- **URL**: `http://localhost:5000`
- **Login**: `acep` / `acep123`
- **Start**: Begin with Dashboard overview

---

## 🛠️ **Installation**

### **Automated Setup (Recommended)**

The `acep_iso_auto_setup.sh` script handles everything automatically:

```bash
# 1. Make executable
chmod +x acep_iso_auto_setup.sh

# 2. Run setup
./acep_iso_auto_setup.sh

# 3. Start application
./run_acep_iso.sh
```

**What the script does:**
- ✅ Detects and installs missing dependencies
- ✅ Creates Python virtual environment
- ✅ Handles externally-managed-environment errors
- ✅ Installs all requirements
- ✅ Sets proper permissions
- ✅ Tests the application
- ✅ Creates quick launcher script

### **Manual Setup**

If you prefer manual installation:

```bash
# 1. Create virtual environment
python3 -m venv acep_iso_venv

# 2. Activate environment
source acep_iso_venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py
```

---

## 📱 **Usage Guide**

### **1. Initial Setup**
- Run the automated setup: `./acep_iso_auto_setup.sh`
- Start the application: `./run_acep_iso.sh`
- Login with default credentials: `acep` / `acep123`
- Database is automatically initialized with all 93 controls

### **2. Dashboard Overview**
- View compliance statistics and progress
- Monitor risk levels and recent activity
- Access quick actions and navigation

### **3. Audit Checklist**
- Review ISO 27001:2022 Annex A controls
- Update control status and add notes
- Track progress and completion rates

### **4. Evidence Management**
- Upload supporting documents and files
- Associate evidence with specific controls
- Organize and search evidence library

### **5. Risk Assessment**
- Add new risks to the register
- Calculate severity scores automatically
- Plan mitigation strategies

### **6. Report Generation**
- Generate comprehensive audit reports
- Customize report content and format
- Export and share results

---

## 🏗️ **Architecture**

### **Technology Stack**
- **Backend**: Python Flask web framework
- **Database**: SQLite for data persistence
- **Frontend**: HTML5 + Bootstrap 5 + Custom CSS
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Styling**: CSS3 with CSS Custom Properties and animations

### **Design Patterns**
- **MVC Architecture**: Model-View-Controller separation
- **RESTful Routes**: Clean, semantic URL structure
- **Template Engine**: Jinja2 for dynamic HTML generation
- **Session Management**: Secure user authentication

---

## 🎨 **UI/UX Features**

### **Modern Tech Theme**
- **Color Scheme**: Deep space blues with cyan accents
- **Gradients**: Tech-inspired linear and radial gradients
- **Glass-morphism**: Transparent cards with backdrop blur
- **Animations**: Smooth, 60fps transitions and effects

### **Latest UI Improvements**
- **Text Visibility**: All text is now properly visible with white color on dark backgrounds
- **Enhanced Descriptions**: Comprehensive ISO 27001 control descriptions for better understanding
- **Performance Optimized**: CSS containment and GPU acceleration for smooth interactions
- **Accessibility Enhanced**: Improved focus states and keyboard navigation support

### **Interactive Elements**
- **Hover Effects**: Cards lift and glow on interaction
- **Status Badges**: Color-coded with animated glow
- **Progress Indicators**: Animated progress bars
- **Responsive Design**: Mobile-first approach

### **Accessibility Features**
- **High Contrast**: WCAG AA compliant color ratios
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader**: Proper ARIA labels and structure
- **Focus Management**: Clear focus indicators

---

## 🔧 **Technical Details**

### **Performance Optimizations**
- **CSS Optimizations**: Reduced repaints and GPU acceleration
- **JavaScript**: Modern ES6+ with performance best practices
- **Image Lazy Loading**: Intersection Observer API
- **Efficient Animations**: Transform and opacity-based transitions

### **Browser Compatibility**
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Support**: Responsive design for all screen sizes
- **Progressive Enhancement**: Graceful degradation for older browsers

### **Security Features**
- **Input Validation**: Server-side and client-side validation
- **SQL Injection Protection**: Parameterized queries
- **XSS Prevention**: Content Security Policy implementation
- **File Upload Security**: Type and size validation

---

## 📊 **Database Schema**

### **Core Tables**
```sql
-- Users table
users (id, username, password_hash, email, created_at)

-- ISO 27001 Controls
controls (id, control_id, title, description, category, status, notes, updated_at)

-- Evidence files
evidence (id, control_id, filename, original_name, file_path, description, uploaded_at)

-- Risk register
risks (id, title, description, likelihood, impact, severity, mitigation, created_at)
```

### **Relationships**
- **Controls** ↔ **Evidence**: One-to-many relationship
- **Users** ↔ **Controls**: Many-to-many through audit sessions
- **Controls** ↔ **Risks**: Many-to-many through risk assessments

---

## 🌐 **API Endpoints**

### **Authentication**
- `POST /login` - User authentication
- `GET /logout` - User logout
- `GET /dashboard` - Main dashboard (protected)

### **Audit Management**
- `GET /audit` - Audit checklist view
- `POST /audit/update` - Update control status
- `GET /audit/export` - Export audit data

### **Evidence Management**
- `GET /evidence` - Evidence overview
- `POST /evidence/upload` - File upload
- `GET /evidence/download/<id>` - File download
- `DELETE /evidence/<id>` - Delete evidence

### **Risk Management**
- `GET /risks` - Risk register view
- `POST /risks/add` - Add new risk
- `PUT /risks/<id>` - Update risk
- `DELETE /risks/<id>` - Delete risk

### **Reporting**
- `GET /reports` - Report generation interface
- `POST /reports/generate` - Generate HTML report
- `GET /reports/download/<id>` - Download report

---

## 📁 **Project Structure**

```
acep-iso-27001-audit/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── acep_iso_auto_setup.sh         # Automated setup script
├── run_acep_iso.sh                # Quick launcher script
├── database/                       # SQLite database files
├── static/                         # Static assets
│   ├── css/
│   │   └── styles.css             # Optimized CSS with tech theme
│   ├── js/
│   │   └── main.js                # Enhanced JavaScript
│   └── uploads/                    # Evidence file storage
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── login.html                 # Authentication page
│   ├── dashboard.html             # Main dashboard
│   ├── audit_checklist.html       # ISO controls checklist
│   ├── evidence.html              # Evidence management
│   ├── risk_register.html         # Risk assessment
│   ├── reports.html               # Report generation
│   └── report.html                # Generated report template
└── README.md                      # This comprehensive documentation
```

---

## 🔒 **Security Features**

### **Authentication & Authorization**
- **Session Management**: Secure session handling with timeouts
- **Password Security**: Hashed passwords using Werkzeug
- **Access Control**: Protected routes and user validation
- **CSRF Protection**: Built-in Flask security features

### **Data Protection**
- **Input Sanitization**: Clean and validate all user inputs
- **SQL Injection Prevention**: Parameterized database queries
- **File Upload Security**: Type validation and size limits
- **XSS Prevention**: Content escaping and validation

---

## 📱 **Responsive Design**

### **Mobile-First Approach**
- **Touch-Friendly**: Large touch targets (44px minimum)
- **Responsive Grid**: Bootstrap 5 responsive system
- **Adaptive Layout**: Optimized for all screen sizes
- **Mobile Navigation**: Collapsible navigation menu

### **Cross-Device Compatibility**
- **Desktop**: Full-featured interface with advanced controls
- **Tablet**: Optimized touch interface
- **Mobile**: Streamlined mobile experience
- **Print**: Print-friendly report layouts

---

## 🚀 **Performance Optimizations**

### **Frontend Optimizations**
- **CSS Performance**: GPU-accelerated animations and transforms with `will-change`, `backface-visibility`, and `transform: translateZ(0)`
- **JavaScript Efficiency**: Modern ES6+ with performance best practices, lazy loading, and Intersection Observer API
- **Image Optimization**: Lazy loading and efficient formats with performance containment
- **Bundle Optimization**: Minified and compressed assets with CSS containment for better rendering performance
- **Accessibility**: Enhanced focus states and reduced motion support for users with accessibility needs

### **Backend Optimizations**
- **Database Efficiency**: Optimized queries and indexing with SQLite best practices
- **Caching Strategy**: Session-based caching for user data and efficient memory usage
- **File Handling**: Efficient file upload and storage with proper cleanup
- **Memory Management**: Proper resource cleanup and management with optimized database connections
- **Error Handling**: Comprehensive error handling with graceful degradation

### **Latest Enhancements**
- **Text Visibility**: Fixed all text color issues to ensure white text is visible on dark backgrounds
- **ISO Control Descriptions**: Enhanced all 93 ISO 27001:2022 Annex A control descriptions with detailed, actionable guidance
- **Performance Containment**: Added CSS containment properties for better rendering performance
- **Accessibility Improvements**: Enhanced focus states and keyboard navigation support

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **1. ModuleNotFoundError: No module named 'flask'**
```bash
# Solution: Activate virtual environment
source acep_iso_venv/bin/activate
pip install -r requirements.txt
```

#### **2. externally-managed-environment Error**
```bash
# Solution: Use the automated setup script
./acep_iso_auto_setup.sh
```

#### **3. Port Already in Use**
```bash
# Solution: Kill existing process or change port
lsof -ti:5000 | xargs kill -9
# Or modify app.py port number
```

#### **4. Database Errors**
```bash
# Solution: Remove and recreate database
rm database/audit.db
python app.py  # Will recreate database
```

### **Performance Issues**
- **Slow Loading**: Check virtual environment activation
- **Memory Issues**: Ensure proper cleanup of file uploads
- **Database Slow**: Verify SQLite file permissions

---

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Code Standards**
- **Python**: PEP 8 compliance
- **JavaScript**: ES6+ with consistent formatting
- **CSS**: BEM methodology and CSS custom properties
- **HTML**: Semantic markup and accessibility

### **Testing**
- **Manual Testing**: Test all user flows
- **Cross-browser**: Verify compatibility
- **Mobile Testing**: Responsive design validation
- **Security Testing**: Input validation and authentication

---

## 📄 **License**

This project is created for educational and professional use. All rights reserved by A Chaitanya Eshwar Prasad.

---

## 👨‍💻 **Creator**

**A Chaitanya Eshwar Prasad** - Cybersecurity Professional & Developer

### **Connect & Follow**
- 🌐 **Website**: [chaitanyaeshwarprasad.com](https://chaitanyaeshwarprasad.com)
- 💼 **LinkedIn**: [linkedin.com/in/chaitanya-eshwar-prasad](https://linkedin.com/in/chaitanya-eshwar-prasad)
- 🐙 **GitHub**: [github.com/chaitanyaeshwarprasad](https://github.com/chaitanyaeshwarprasad)
- 🎥 **YouTube**: [youtube.com/@chaitanya.eshwar.prasad](https://youtube.com/@chaitanya.eshwar.prasad)
- 📸 **Instagram**: [instagram.com/acep.tech.in.telugu](https://instagram.com/acep.tech.in.telugu)
- 🛡️ **YesWeHack**: [yeswehack.com/hunters/chaitanya-eshwar-prasad](https://yeswehack.com/hunters/chaitanya-eshwar-prasad)

### **About the Creator**
A passionate cybersecurity professional with expertise in information security management systems, penetration testing, and secure software development. Committed to creating tools that make cybersecurity accessible and efficient for professionals worldwide.

---

<div align="center">

**🎉 Thank you for choosing ACEP ISO 27001 Audit Assistant!**

*Empowering cybersecurity professionals with modern, efficient audit tools.*

[![Star](https://img.shields.io/badge/⭐_Star_this_repo-important?style=for-the-badge&logo=github)](https://github.com/chaitanyaeshwarprasad)
[![Fork](https://img.shields.io/badge/🍴_Fork_this_repo-success?style=for-the-badge&logo=github)](https://github.com/chaitanyaeshwarprasad)

</div>
