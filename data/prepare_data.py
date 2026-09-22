import json

DATASET = [
    # INVOICES
    {
        "text": "Acme Industrial Supplies\n123 Market St, Suite 400, Austin TX\nINVOICE\nInvoice Number: INV-2026-001\nDate: 12-05-2026\nDue Date: 12-06-2026\nBilled To: Globex Corp\nDescription: Cloud hosting and database maintenance\nQty: 1 Unit Price: $1,250.00\nSubtotal: $1,250.00\nTax: $100.00\nTotal Amount: $1,350.00\nPayment Terms: Net 30 days. Thank you for your business!",
        "label": "Invoice"
    },
    {
        "text": "Apex Consulting LLC\nTax Invoice / Receipt\nInvoice #: 88472\nInvoice Date: 2026-03-14\nCustomer: Horizon Media Group\nServices Rendered: Security audit, penetration testing, compliance checklist.\nHours: 40 Rate: $150/hr\nTotal Due: $6,000.00\nBank Transfer Details: Apex Bank, Account 987654321, Routing 123456.",
        "label": "Invoice"
    },
    {
        "text": "Starlight Office Stationery Ltd\nBILL / CASH MEMO\nBill No: ST-9021\nDated: 15/08/2026\nBuyer: Zenith Technologies\nItem 1: Ergonomic Desk Chairs x 5 = $1,500.00\nItem 2: Whiteboards x 2 = $300.00\nDelivery Fee: $50.00\nGrand Total: $1,850.00\nPlease pay within 15 days.",
        "label": "Invoice"
    },
    {
        "text": "Quantum Logistics & Shipping\nFREIGHT INVOICE\nInv No: QL-4491-X\nIssue Date: 04-11-2026\nConsignee: Metro Distribution Hub\nCargo: Electronic components 400kg\nFreight charge: $820.00\nFuel surcharge: $95.00\nBalance Due: $915.00\nRemit payment to payment@quantumlogistics.com",
        "label": "Invoice"
    },
    {
        "text": "Vertex Software Solutions\nCommercial Invoice\nInvoice Number: INV-89231\nDate: October 05, 2026\nClient: Pacific Retailers Ltd\nLicense fee for ERP platform: $4,500.00\nImplementation support: $1,200.00\nTotal Amount: $5,700.00\nAll payments are non-refundable. Paid via Wire Transfer.",
        "label": "Invoice"
    },
    {
        "text": "FastPrint Media\nInvoice ID: FP-1092\nDate: 01/09/2026\nBilled By: FastPrint Solutions\nOrder: Brochure design and marketing banner print run.\nTotal: $640.00\nPaid in Full. Payment method: Credit Card ending 4412.",
        "label": "Invoice"
    },
    {
        "text": "BlueSky Web Design Studio\nINVOICE\nInvoice Number: BS-2026-44\nDate: 02-09-2026\nTo: Bright Horizon Schools\nWeb development, UI UX wireframes, hosting setup.\nTotal Amount: $2,400.00\nPlease make payment by September 30, 2026.",
        "label": "Invoice"
    },
    {
        "text": "Pacific Hardware Wholesale\nTax Invoice\nInv #: PHW-3301\nDate: 2026-06-20\nSold to: Delta Construction Ltd\nRaw steel pipes, fittings, valves.\nSubtotal: $8,400.00\nVAT (10%): $840.00\nTotal: $9,240.00\nPayment received with thanks.",
        "label": "Invoice"
    },
    {
        "text": "Catering By Olivia\nEVENT INVOICE\nInvoice Number: CBO-771\nDate: 18-07-2026\nBill To: Silverline Corporate Retreat\nFood service for 120 guests, beverage package, servers.\nTotal Amount: $3,750.00\nDeposit paid: $1,000.00\nRemaining Total: $2,750.00",
        "label": "Invoice"
    },
    {
        "text": "CyberShield Defense Inc.\nSUBSCRIPTION INVOICE\nInvoice Number: CS-99120\nDate: 2026-01-10\nCustomer: FinTech Global\nAnnual Endpoint Detection & Response (EDR) License.\nTotal: $12,000.00\nStatus: UNPAID. Due within 30 days.",
        "label": "Invoice"
    },

    # RESUMES
    {
        "text": "Sarah Connor\nsarah.connor@example.com | (555) 234-5678 | San Francisco, CA\nSUMMARY\nExperienced Senior Machine Learning Engineer with 6+ years deploying deep learning models in production.\nEXPERIENCE\nAI Research Labs - Lead ML Engineer (2022 - Present)\n- Built NLP recommendation pipeline using PyTorch, Transformers, and FastAPI.\n- Reduced model latency by 45% using TensorRT and ONNX runtime.\nDataWorks - Data Scientist (2019 - 2022)\n- Trained scikit-learn classification models on 10M+ records.\nSKILLS\nPython, PyTorch, TensorFlow, Scikit-Learn, Docker, Kubernetes, AWS, SQL, Git, Linux.\nEDUCATION\nB.S. in Computer Science, Stanford University.",
        "label": "Resume"
    },
    {
        "text": "David Chen\nEmail: david.chen@techdev.org\nPhone: +1-617-987-6543\nBoston, MA\nPROFESSIONAL PROFILE\nFull Stack Web Developer specializing in React, Node.js, and cloud architectures.\nWORK HISTORY\nCloudWave Solutions - Full Stack Developer (2021 - Present)\n- Developed responsive web applications using React, TypeScript, and Tailwind CSS.\n- Built RESTful APIs and microservices with Node.js, Express, and PostgreSQL.\nInnovatech - Frontend Developer (2018 - 2021)\n- Created user interfaces with Vue.js and Redux.\nTECHNICAL SKILLS\nJavaScript, TypeScript, React, Node.js, Express, PostgreSQL, MongoDB, Docker, Git, CI/CD.\nEDUCATION\nM.S. in Software Engineering, Northeastern University.",
        "label": "Resume"
    },
    {
        "text": "Priya Sharma\npriya.sharma@domain.com | +91 9876543210 | Bangalore, India\nOBJECTIVE\nData Analyst seeking to leverage expertise in data visualization, SQL queries, and Python automation.\nEXPERIENCE\nAnalytics Corp - Data Analyst (2023 - Present)\n- Designed interactive executive dashboards in Tableau and Power BI.\n- Automated weekly ETL reporting using Python, Pandas, and MySQL.\nInfosys - Junior Analyst (2021 - 2023)\n- Performed statistical data cleaning and hypothesis testing with R and Python.\nCORE COMPETENCIES\nPython, SQL, Tableau, Power BI, Pandas, NumPy, Data Analysis, Excel, Git.\nEDUCATION\nBachelor of Technology, NIT Karnataka.",
        "label": "Resume"
    },
    {
        "text": "Marcus Johnson\nmarcus.j@cybersecmail.com | 312-555-0199 | Chicago, IL\nCAREER OBJECTIVE\nDevOps and Cloud Infrastructure Engineer with proven track record in automating multi-cloud environments.\nEMPLOYMENT\nInfraOps LLC - DevOps Engineer (2020 - Present)\n- Created Terraform infrastructure-as-code scripts for AWS and Azure.\n- Orchestrated CI/CD pipelines with GitHub Actions, Jenkins, and Kubernetes.\nSKILLS & TOOLS\nAWS, Azure, Docker, Kubernetes, Terraform, Ansible, Linux, Bash, Python, CI/CD, Git.\nEDUCATION\nB.Sc. in Computer Networking, University of Illinois.",
        "label": "Resume"
    },
    {
        "text": "Elena Rostova\nContact: elena.rostova@designlab.io | (415) 321-7654\nPORTFOLIO & RESUME\nSenior UI/UX Designer and Frontend Specialist.\nEXPERIENCE\nCreative Minds Studio - Product Designer (2020 - Present)\n- Led user research, usability testing, and wireframe prototypes for SaaS products.\n- Collaborated with developers using React, HTML, and CSS.\nSKILLS\nFigma, Adobe XD, HTML, CSS, JavaScript, React, User Research, Wireframing, Agile, Scrum.\nEDUCATION\nB.A. in Digital Arts, UC Berkeley.",
        "label": "Resume"
    },
    {
        "text": "Michael Kevin Brown\nEmail: michael.brown@fintechcode.com | Tel: 206-555-4321\nSeattle, WA\nOBJECTIVE: Senior Backend Software Engineer\nWORK EXPERIENCE\nAmazon - Software Development Engineer II (2021 - Present)\n- Architected high-throughput microservices using Go and Java.\n- Managed distributed message queues using Kafka and RabbitMQ.\nSKILLS\nGo, Golang, Java, Spring Boot, Kafka, Redis, AWS, Docker, Kubernetes, SQL, REST API, Git.\nEDUCATION\nB.S. in Computer Engineering, University of Washington.",
        "label": "Resume"
    },
    {
        "text": "Ananya Patel\nananya.patel@biotechai.org | (734) 555-9012\nAnn Arbor, MI\nBIOINFORMATICS & AI RESEARCHER\nExperience:\nGenomics Institute - Research Fellow (2022 - Present)\n- Analyzed large-scale gene sequencing datasets with Python, SciPy, and Biopython.\n- Built deep convolutional neural networks in TensorFlow for protein folding prediction.\nSkills:\nPython, R, TensorFlow, Keras, Machine Learning, Deep Learning, Pandas, Git, Linux.\nEducation:\nPh.D. in Bioinformatics, University of Michigan.",
        "label": "Resume"
    },
    {
        "text": "Robert Tyler Vance\nrobert.vance@enterprisesys.com | 214-555-8833 | Dallas, TX\nSUMMARY\nDatabase Administrator & System Architect with 8 years ensuring high-availability database performance.\nWORK HISTORY\nTexas Financial Systems - Senior DBA (2018 - Present)\n- Managed 50+ PostgreSQL and MySQL clusters handling 20,000 queries/second.\n- Optimized query execution plans and database sharding.\nTECHNICAL PROFICIENCIES\nPostgreSQL, MySQL, Oracle, MongoDB, Redis, Linux, Bash, Python, Docker.\nEDUCATION\nB.S. in Information Systems, UT Dallas.",
        "label": "Resume"
    },
    {
        "text": "Jessica Taylor\njessica.taylor@mobileapp.dev | (512) 555-6789 | Austin, TX\nMOBILE APPLICATION DEVELOPER\nExperience:\nAppCraft Studios - Mobile Engineer (2021 - Present)\n- Developed cross-platform iOS and Android apps using Flutter and Dart.\n- Integrated RESTful backend endpoints and Firebase authentication.\nSKILLS: Flutter, Dart, Swift, Kotlin, React Native, Firebase, Git, Jira, Agile.\nEducation: B.S. in Computer Science, UT Austin.",
        "label": "Resume"
    },
    {
        "text": "Liam James O'Connor\nliam.oconnor@embeddedembedded.io | (408) 555-3344 | San Jose, CA\nEMBEDDED SYSTEMS SOFTWARE ENGINEER\nEXPERIENCE\nSilicon Valley Microdevices - Firmware Engineer (2019 - Present)\n- Programmed ARM Cortex microcontrollers in C and C++ for IoT sensor devices.\n- Developed RTOS drivers for I2C, SPI, and UART protocols.\nSKILLS: C, C++, Rust, Embedded Linux, RTOS, Git, Python, Circuit Debugging.\nEDUCATION: M.S. in Electrical and Computer Engineering, San Jose State University.",
        "label": "Resume"
    },

    # OTHER (Non-invoices, non-resumes: NDAs, articles, medical reports, user manuals, policy letters)
    {
        "text": "NON-DISCLOSURE AGREEMENT (NDA)\nThis Mutual Non-Disclosure Agreement is entered into by and between Alpha Corp and Beta Inc.\n1. Confidential Information: Both parties agree to protect and not disclose proprietary data.\n2. Non-Use: Neither party will use confidential data for any purpose other than the business relationship.\n3. Term: This agreement remains in effect for 3 years from execution.\nSignatures:\nAuthorized Signature, Alpha Corp.\nAuthorized Signature, Beta Inc.",
        "label": "Other"
    },
    {
        "text": "Patient Medical Discharge Summary\nPatient ID: PT-49821\nAttending Physician: Dr. Gregory House, M.D.\nDiagnosis: Acute Bronchitis\nTreatment Plan: Prescribed Amoxicillin 500mg three times daily for 7 days. Advised complete bed rest, hydration, and steam inhalation.\nFollow-up appointment scheduled in 10 days at Community Health Clinic.\nEmergency contact: (555) 888-9999.",
        "label": "Other"
    },
    {
        "text": "EMPLOYEE HANDBOOK & COMPANY POLICY\nChapter 4: Working Hours and Remote Work Policy\nEmployees are expected to core hours between 10:00 AM and 4:00 PM EST.\nRequests for remote work must be submitted to human resources 14 days in advance.\nPaid time off (PTO) accrues at a rate of 1.5 days per month worked.\nPlease refer to the HR portal for benefits enrollment.",
        "label": "Other"
    },
    {
        "text": "ACADEMIC RESEARCH PAPER\nTitle: Neural Machine Translation with Attention Mechanisms: A Review\nAbstract: We examine sequence-to-sequence neural networks applied to multi-language translation.\nEmpirical results show that self-attention layers outperform recurrent architectures across BLEU benchmark scores.\nKeywords: Attention, NLP, Deep Learning, Transformers, Linguistics.\nPublished in IEEE Transactions on Signal Processing, 2026.",
        "label": "Other"
    },
    {
        "text": "Residential Tenancy Rental Lease Agreement\nLandlord: Greenfield Property Management LLC\nTenant: Jonathan Miller\nPremises: 742 Evergreen Terrace, Springfield\nTerm: 12 months beginning November 1, 2026.\nRent: $1,400 per month due on the first calendar day.\nSecurity Deposit: $1,400 held in escrow.\nNo pets without prior written consent.",
        "label": "Other"
    },
    {
        "text": "Wireless Bluetooth Speaker User Manual\nModel: BT-SoundBox 500\nPackage Contents: Speaker, Type-C charging cable, 3.5mm AUX wire, quick guide.\nPairing instructions: Turn on the power switch. The blue LED will flash. Open Bluetooth settings on your mobile device and select 'SoundBox-500'.\nWarning: Do not submerge into water exceeding 1 meter depth.",
        "label": "Other"
    },
    {
        "text": "Meeting Minutes - Board of Directors\nDate: September 10, 2026\nChair: Catherine Walker\nAttendees: 7 board members present.\nAgenda Items:\n1. Approval of Q2 financial statements.\n2. Expansion into European markets scheduled for Q1 2027.\n3. Appointment of internal audit committee.\nAdjournment: The meeting adjourned at 4:30 PM.",
        "label": "Other"
    },
    {
        "text": "Press Release - TechNova Inc Announces Breakthrough in Solid State Batteries\nFOR IMMEDIATE RELEASE\nTechNova Inc today announced a new solid-state battery architecture offering 600 miles of vehicle range on a single 10-minute charge.\nCommercial production is slated for late 2027.\nMedia Contact: press@technovainc.org | (555) 777-1234.",
        "label": "Other"
    },
    {
        "text": "Terms of Service and End User License Agreement (EULA)\nBy accessing or downloading this software application, you agree to be bound by the following conditions.\nYou may not reverse engineer, decompile, or modify the binary.\nThe software is provided as-is without warranty of merchantability or fitness for a particular purpose.",
        "label": "Other"
    },
    {
        "text": "Flight Itinerary and Electronic Ticket Receipt\nPassenger: Alexander Wright\nBooking Reference: PNR-789X\nAirline: Global Skyways Flight GS-104\nDeparture: JFK New York (08:30 AM) -> Arrival: LHR London Heathrow (08:45 PM)\nSeat: 14A (Window) | Class: Economy\nBaggage: 1 checked bag up to 23kg.",
        "label": "Other"
    }
]

with open("data/documents_dataset.json", "w", encoding="utf-8") as f:
    json.dump(DATASET, f, indent=2)

print(f"Created dataset with {len(DATASET)} balanced document examples.")
