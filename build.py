#!/usr/bin/env python3
"""Generate the EcoBuilders site. Run from the repo root: python3 build.py"""
import os, json, html

OUT = os.path.dirname(os.path.abspath(__file__))

MAIL = "mailto:info@buildecoenergy.com?subject=Project%20Inquiry%20-%20EcoBuilders"

# --------------------------------------------------------------------------
# Head / chrome partials
# --------------------------------------------------------------------------

def head(title, desc, root):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#F4F6F4">
  <!-- Sets the theme before first paint so dark-mode visitors never see a white flash. -->
  <script>(function(){{try{{var s=localStorage.getItem('eb-theme');
  document.documentElement.setAttribute('data-theme',
    s||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));}}
  catch(e){{document.documentElement.setAttribute('data-theme','light');}}}})();</script>
  <link rel="stylesheet" href="{root}styles.css">
</head>
<body>'''


def header(root, home_prefix):
    return f'''
  <header>
    <div class="container nav">
      <a href="{home_prefix}index.html" class="logo-link">
        <img class="nav-logo-mark logo-on-light" src="{root}assets/ecobuilders-mark-dark.png" alt="">
        <img class="nav-logo-mark logo-on-dark" src="{root}assets/ecobuilders-mark-white.png" alt="">
        <span class="nav-logo-text">EcoBuilders</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav-links">
        <a href="{home_prefix}index.html#services">Services</a>
        <a href="{home_prefix}index.html#about">About</a>
        <a href="{home_prefix}index.html#markets">Markets</a>
        <a href="{home_prefix}index.html#contact">Contact</a>
        <a class="btn btn-primary" href="{MAIL}">Request a Proposal</a>
        <button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
      </nav>
    </div>
  </header>
'''


def footer(root):
    return f'''
  <footer>
    <div class="container footer-grid">
      <div>
        <div class="logo-link">
          <img class="nav-logo-mark logo-on-light" src="{root}assets/ecobuilders-mark-dark.png" alt="">
          <img class="nav-logo-mark logo-on-dark" src="{root}assets/ecobuilders-mark-white.png" alt="">
          <span class="nav-logo-text">EcoBuilders</span>
        </div>
        <p>Commercial EV charging, solar, energy storage, commissioning, O&amp;M and smart controls.</p>
      </div>
      <div>
        <strong>Contact</strong>
        <p>Noah Schij<br>
          <a href="mailto:info@buildecoenergy.com">info@buildecoenergy.com</a><br>
          <button type="button" class="phone-reveal">Click to show number</button></p>
      </div>
      <div>
        <strong>License</strong>
        <p>#889419</p>
      </div>
    </div>
  </footer>
'''


GALLERY_MODAL = '''
  <div id="galleryModal" hidden role="dialog" aria-modal="true" aria-labelledby="galleryTitle">
    <div class="gallery-backdrop"></div>
    <div class="gallery-panel">
      <div class="gallery-stage">
        <button class="gallery-close" type="button" aria-label="Close gallery">&times;</button>
        <button class="gallery-nav prev" type="button" aria-label="Previous image">&#8249;</button>
        <img id="galleryMainImg" alt="">
        <button class="gallery-nav next" type="button" aria-label="Next image">&#8250;</button>
      </div>
      <div class="gallery-meta">
        <h3 id="galleryTitle"></h3>
        <p id="galleryDesc"></p>
      </div>
      <div class="gallery-thumbs" id="galleryThumbs"></div>
    </div>
  </div>
'''


def tail(root):
    return f'''{GALLERY_MODAL}
  <script src="{root}site.js"></script>
</body>
</html>
'''

# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------
# title  : what it is + city
# specs  : the numbers
# note   : one line of scope
# images : [(file, caption)] — first is the thumbnail

P = {
 # ---- DC fast
 "dcfast-bakersfield": dict(
    title="4 Dual-Port DC Fast Chargers · Bakersfield, CA",
    specs="8 connectors · CCS / CHAdeMO / NACS",
    note="Service equipment work and charger commissioning at a retail entertainment site.",
    images=[("dcfast-bakersfield.jpg", "Arc-flash rated work inside the pad-mount switchgear feeding the charger.")]),
 "dcfast-blythe": dict(
    title="2 DC Fast + 2 Level 2 · Blythe, CA",
    specs="Power cabinet · 2 satellite dispensers",
    note="Highway corridor site along the I-10 route.",
    images=[("dcfast-blythe.jpg", "Power cabinet feeding two satellite dispensers.")]),
 "dcfast-chula-vista": dict(
    title="8-Port DC Fast Hub · Chula Vista, CA",
    specs="8 ports · 200 kW · battery buffered",
    note="Charging hub built into an operating retail fuel site.",
    images=[("dcfast-chula-vista.jpg", "Charger row alongside the fuel canopy.")]),
 "dcfast-corridor": dict(
    title="Highway Corridor Charging Sites · California",
    specs="Multiple locations · DC fast",
    note="Service equipment, pads and charger setting across corridor sites.",
    images=[("dcfast-corridor-set.jpg", "Charger cabinet craned onto its pad."),
            ("sitework-trench.jpg", "Trenching and conduit routing across the lot."),
            ("sitework-equipment-pad.jpg", "Precast equipment pad set over the conduit stub-ups.")]),

 # ---- multifamily
 "mf-paradise": dict(
    title="25 Pedestals, Senior Affordable Housing · Paradise, CA",
    specs="25 pedestals · Level 2",
    note="Charging across a rebuilt affordable senior community.",
    images=[("multifamily-paradise.jpg", "Setting and terminating pedestals along the new curb line.")]),
 "mf-long-beach": dict(
    title="Residential Tower Charging · Long Beach, CA",
    specs="Chargers, pedestals and feeder replacement",
    note="Retrofit and service inside an occupied high-rise parking structure.",
    images=[("multifamily-long-beach.jpg", "Commissioning chargers on the parking level.")]),
 "mf-broomfield": dict(
    title="4 Pedestals / 8 Outlets · Broomfield, CO",
    specs="4 pedestals · 8 outlets",
    note="Structured-parking installation including wire pull and conduit modifications.",
    images=[("multifamily-broomfield.jpg", "Anchoring a pedestal to the deck."),
            ("multifamily-broomfield-conduit.jpg", "Overhead conduit run under the parking deck.")]),
 "mf-brea": dict(
    title="Multifamily Charging Service · Brea, CA",
    specs="Breaker replacement · megger testing · feeders",
    note="Ongoing service across a large mixed-use community.",
    images=[("multifamily-brea.jpg", "Commissioning a charger in the resident courtyard."),
            ("multifamily-outlet.jpg", "Metered outlet and conduit at a resident stall.")]),
 "mf-folsom": dict(
    title="Multifamily Charging · Folsom, CA",
    specs="Level 2 · lot-wide distribution",
    note="Underground distribution and charger installation across the parking areas.",
    images=[("multifamily-folsom.jpg", "Site-wide trenching and conduit work underway.")]),
 "mf-riverside": dict(
    title="Multifamily Charging · Riverside, CA",
    specs="Level 2 · pedestals and EVSE",
    note="Ongoing charging installation and support at a new community.",
    images=[("multifamily-riverside.jpg", "Carport construction over the charging bays."),
            ("multifamily-pedestals.jpg", "Pedestal row set along the resident parking bays.")]),

 # ---- workplace & campus
 "campus-san-diego": dict(
    title="Corporate Campus · San Diego, CA",
    specs="121 Level 2 ports · 960 kW solar carport · 280 kW / 540 kWh storage",
    note="Integrated charging, solar carport and battery storage on one campus.",
    images=[("campus-san-diego.jpg", "Rigging battery equipment into place."),
            ("solar-carport.jpg", "Solar carport canopies over the parking field.")]),
 "hospital-montebello": dict(
    title="Hospital Charging · Montebello, CA",
    specs="50 Level 2 ports",
    note="Charging under solar carports at a working medical campus.",
    images=[("hospital-montebello.jpg", "Charger work beneath the solar carport.")]),
 "hospital-irwindale": dict(
    title="Hospital Charging · Irwindale, CA",
    specs="26 Level 2 ports",
    note="Campus-wide distribution and charger installation.",
    images=[("hospital-irwindale.jpg", "Cable pull across the campus parking field.")]),
 "hospital-baldwin-park": dict(
    title="Hospital Charging · Baldwin Park, CA",
    specs="Level 2 · parking structure",
    note="Conduit distribution and wall-mounted chargers through a parking structure.",
    images=[("hospital-baldwin-park.jpg", "Conduit run feeding the charger row.")]),
 "hospital-diamond-bar": dict(
    title="Hospital Charging · Diamond Bar, CA",
    specs="Level 2 · staff and visitor",
    note="Charging installation supporting staff and visitor parking.",
    images=[("hospital-diamond-bar.jpg", "Completed charging stalls.")]),
 "campus-la-jolla": dict(
    title="Research Campus Charging · La Jolla, CA",
    specs="Level 2 · carport charging",
    note="Charging integrated under the solar canopies.",
    images=[("solar-research-la-jolla.jpg", "Charging stalls beneath the carport canopies.")]),
 "museum-los-angeles": dict(
    title="Museum Campus Charging · Los Angeles, CA",
    specs="Level 2 · visitor and staff",
    note="Charging infrastructure across a cultural campus.",
    images=[("museum-los-angeles.jpg", "Campus charging installation.")]),

 # ---- fleet
 "fleet-san-diego": dict(
    title="Parcel Fleet Depot · San Diego, CA",
    specs="DC fast · depot charging",
    note="Depot charging for an electric delivery fleet.",
    images=[("fleet-san-diego.jpg", "Depot charging infrastructure.")]),
 "fleet-torrance": dict(
    title="Fleet & Workplace Charging · Torrance, CA",
    specs="DC fast + Level 2",
    note="Charger installation and service across fleet and employee parking.",
    images=[("fleet-torrance.jpg", "Servicing a mobile DC fast unit at the yard."),
            ("fleet-torrance-2.jpg", "Terminating a charger pedestal in the employee lot.")]),

 # ---- solar
 "solar-winery-roof": dict(
    title="Winery Rooftop Array · Napa, CA",
    specs="Rooftop solar · hybrid microgrid",
    note="Part of a solar, storage and generator microgrid serving winery operations.",
    images=[("solar-winery-roof.jpg", "Rooftop array serving the winery.")]),
 "solar-winery-ground": dict(
    title="Winery Ground-Mount Array · Napa, CA",
    specs="Ground-mount solar",
    note="Ground-mount generation feeding the same hybrid microgrid.",
    images=[("solar-winery-ground.jpg", "Ground-mount array.")]),
 "solar-research": dict(
    title="Research Campus Solar · La Jolla, CA",
    specs="Rooftop and carport arrays",
    note="Solar across parking canopies and building roofs on a coastal research campus.",
    images=[("solar-research-la-jolla.jpg", "Carport canopies and rooftop arrays across the campus.")]),
 "solar-carport-sd": dict(
    title="Solar Carport, Corporate Campus · San Diego, CA",
    specs="960 kW carport canopies",
    note="Carport canopies combining covered parking with on-site generation.",
    images=[("solar-carport.jpg", "Completed carport canopies."),
            ("solar-carport-build.jpg", "Setting modules on the carport structure."),
            ("sitework-core-drill.jpg", "Core drilling for conduit stub-ups.")]),

 # ---- storage
 "storage-san-diego": dict(
    title="Battery Storage, Corporate Campus · San Diego, CA",
    specs="280 kW / 540 kWh · Megapack",
    note="Storage paired with a 960 kW solar carport and 121 charging ports.",
    images=[("campus-san-diego.jpg", "Megapack rigged into position over the pad.")]),
 "storage-torrance": dict(
    title="1 MWh Battery Storage · Torrance, CA",
    specs="1 MWh · fleet depot",
    note="Storage supporting depot charging load.",
    images=[("storage-torrance.jpg", "Battery enclosure craned onto its pad.")]),
 "storage-winery": dict(
    title="Hybrid Microgrid · Napa, CA",
    specs="Solar · storage · generator",
    note="Storage and generation integrated so the winery rides through outages.",
    images=[("storage-winery.jpg", "Inspection and documentation inside the power cabinet.")]),

 # ---- commissioning
 "comm-setup": dict(
    title="Pre-Energization Setup",
    specs="Integration · settings · monitoring",
    note="Equipment integration, control settings and monitoring configured before energization.",
    images=[("commissioning-setup.jpg", "Test setup ahead of energization.")]),
 "comm-energize": dict(
    title="Energization & Turnover",
    specs="Energize · QA/QC · documentation",
    note="Safe energization, functional checks and documented turnover.",
    images=[("commissioning-energize.jpg", "Energization and functional checks.")]),
 "comm-termination": dict(
    title="Terminations & Torque Verification",
    specs="Torque-verified terminations",
    note="Documented terminations at distribution equipment.",
    images=[("commissioning-termination.jpg", "Torque verification at the panel."),
            ("sitework-cable-pull.jpg", "Feeder pull into the gear.")]),
 "comm-winery": dict(
    title="Microgrid Commissioning · Napa, CA",
    specs="Solar · storage · generator",
    note="Functional testing and documentation of the integrated system.",
    images=[("storage-winery.jpg", "Inspection and checklist inside the power cabinet."),
            ("controls-winery.jpg", "System configuration at the cabinet.")]),

 # ---- O&M
 "om-inverter": dict(
    title="Insulation Resistance Testing",
    specs="Commissioning · corrective maintenance",
    note="DC circuits tested before energizing.",
    images=[("om-inverter-test.jpg", "Insulation resistance testing at the inverter.")]),
 "om-pasadena": dict(
    title="School Campus Solar Service · Pasadena, CA",
    specs="Preventive and corrective",
    note="Service at carport-mounted solar equipment.",
    images=[("om-pasadena.jpg", "Service call at a carport-mounted combiner.")]),
 "om-iv": dict(
    title="I-V Curve Tracing",
    specs="String-level performance verification",
    note="Documented testing supporting warranty and performance compliance.",
    images=[("om-iv-tracer.jpg", "String-level I-V curve tracing.")]),
 "om-thermal": dict(
    title="Aerial Thermal Imaging",
    specs="Infrared array inspection",
    note="Aerial thermal scanning for proactive hazard and fault detection.",
    images=[("om-thermal-aerial.jpg", "Aerial infrared scan of the array.")]),
 "om-charging": dict(
    title="EV Charging Service",
    specs="Corrective and preventive",
    note="Diagnostics, electrical repairs and uptime support across charging portfolios.",
    images=[("multifamily-long-beach.jpg", "Diagnostics on an occupied-building charging system."),
            ("multifamily-brea.jpg", "Service visit at a multifamily community.")]),

 # ---- controls
 "controls-ems": dict(
    title="Edge Energy Management",
    specs="Modbus · OCPP · TCP",
    note="Edge systems coordinating solar, storage and charging as one site.",
    images=[("controls-ems.jpg", "Edge EMS installation.")]),
 "controls-ct": dict(
    title="Dynamic Load Management",
    specs="CT-based metering",
    note="Live load data driving charging limits, demand management and reporting.",
    images=[("controls-ct.jpg", "Rope CT installation for load metering.")]),
 "controls-winery": dict(
    title="Microgrid Controls · Napa, CA",
    specs="Solar · storage · generator",
    note="Configuration and integration so generation, storage and loads respond together.",
    images=[("controls-winery.jpg", "System configuration at the power cabinet.")]),
}


def project_html(key, root):
    p = P[key]
    imgs = [{"src": root + "assets/" + f, "caption": c} for f, c in p["images"]]
    data = html.escape(json.dumps(imgs), quote=True)
    count = len(imgs)
    label = f"{count} photos" if count > 1 else "1 photo"
    return f'''          <article class="project-item">
            <button class="project-thumb" type="button" data-images="{data}"
                    data-title="{html.escape(p["title"], quote=True)}"
                    data-specs="{html.escape(p["specs"], quote=True)}"
                    aria-label="Open gallery: {html.escape(p["title"], quote=True)} ({label})">
              <img src="{root}assets/{p["images"][0][0]}" alt="{html.escape(p["title"], quote=True)}" loading="lazy">
            </button>
            <div class="project-body">
              <h4>{p["title"]}</h4>
              <p class="specs">{p["specs"]}</p>
              <p>{p["note"]}</p>
            </div>
          </article>
'''


def section(heading, keys, root):
    items = "".join(project_html(k, root) for k in keys)
    return f'''        <div class="subservice">
          <div class="subservice-head">
            <h3>{heading}</h3>
            <span class="count">{len(keys)} projects</span>
          </div>
          <div class="project-row">
{items}          </div>
        </div>
'''


def flat_row(keys, root):
    items = "".join(project_html(k, root) for k in keys)
    return f'''        <div class="project-row">
{items}        </div>
'''


def cta():
    return f'''        <div class="page-cta">
          <p>Have a site to discuss?<span>Budget pricing, site walks and scope review.</span></p>
          <a class="btn btn-primary" href="{MAIL}">Request a Proposal</a>
        </div>
'''

# --------------------------------------------------------------------------
# Service pages
# --------------------------------------------------------------------------

SERVICES = [
  dict(file="ev-charging.html", name="EV Charging Infrastructure",
       title="EV Charging Infrastructure | EcoBuilders",
       desc="Commercial EV charging installation, commissioning and service for multifamily, healthcare, workplace and fleet sites.",
       lead="EcoBuilders installs and commissions EV charging systems for multifamily, workplace, fleet, and commercial sites. "
            "Charging speed is synced to real site conditions based on solar, battery status, utility rates, and fleet routes.",
       sections=[("DC Fast Charging", ["dcfast-bakersfield", "dcfast-blythe", "dcfast-chula-vista", "dcfast-corridor"]),
                 ("Multifamily", ["mf-paradise", "mf-long-beach", "mf-broomfield", "mf-brea", "mf-folsom", "mf-riverside"]),
                 ("Workplace & Campus", ["campus-san-diego", "hospital-montebello", "hospital-irwindale",
                                          "hospital-baldwin-park", "hospital-diamond-bar", "campus-la-jolla", "museum-los-angeles"]),
                 ("Fleet Depot", ["fleet-san-diego", "fleet-torrance"])]),

  dict(file="commercial-solar.html", name="Commercial Solar",
       title="Commercial Solar | EcoBuilders",
       desc="Electrical and construction support for commercial rooftop, carport and ground-mount solar, including interconnection.",
       lead="EcoBuilders provides electrical and construction support for commercial solar across rooftop, canopy, and ground-mount "
            "systems, including interconnection so solar integrates with other onsite technology.",
       flat=["solar-carport-sd", "solar-winery-roof", "solar-winery-ground", "solar-research"]),

  dict(file="energy-storage.html", name="Energy Storage",
       title="Energy Storage | EcoBuilders",
       desc="Commercial battery energy storage construction support, equipment setting, electrical integration and interconnection.",
       lead="Energy storage lets sites capture excess solar, cut demand charges, improve resilience, and support larger loads. "
            "EcoBuilders delivers construction support from site preparation and equipment setting to electrical integration and interconnection.",
       flat=["storage-san-diego", "storage-torrance", "storage-winery"]),

  dict(file="commissioning.html", name="Commissioning",
       title="Commissioning | EcoBuilders",
       desc="Structured startup, functional testing and documentation so systems are verified, safe and warranty-compliant.",
       lead="Proper commissioning protects the investment and reduces callbacks. EcoBuilders performs structured startup, "
            "functional testing, and documentation so systems are verified, safe, and warranty-compliant.",
       flat=["comm-setup", "comm-energize", "comm-termination", "om-inverter", "comm-winery"]),

  dict(file="om.html", name="O&amp;M",
       title="O&M | EcoBuilders",
       desc="Monitoring, preventive and corrective maintenance keeping charging, solar and storage systems online and compliant.",
       lead="Long-term performance depends on consistent monitoring and reliable field response. EcoBuilders keeps systems online, "
            "productive, safe, and compliant.",
       flat=["om-charging", "om-pasadena", "om-iv", "om-thermal"]),

  dict(file="smart-controls.html", name="Smart Controls &amp; Energy Management",
       title="Smart Controls & Energy Management | EcoBuilders",
       desc="Edge energy management and load management coordinating solar, storage and EV charging over Modbus, OCPP and TCP.",
       lead="Smart controls use real-time data to manage loads and coordinate solar, storage, and EV charging. "
            "Edge systems act as a local hub over Modbus, OCPP, and TCP.",
       flat=["controls-ems", "controls-ct", "controls-winery"]),
]


def build_service(s):
    root, home = "../", "../"
    if "sections" in s:
        body = "".join(section(h, k, root) for h, k in s["sections"])
    else:
        body = flat_row(s["flat"], root)

    return (head(s["title"], s["desc"], root)
            + header(root, home)
            + f'''
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="{home}index.html">Home</a> / <a href="{home}index.html#services">Services</a> / {s["name"]}</div>
      <h1>{s["name"]}</h1>
      <p class="lead">{s["lead"]}</p>
    </div>
  </section>

  <section class="service-content">
    <div class="container">
      <div class="eyebrow">Project Experience</div>
{body}{cta()}      <a href="{home}index.html#services" class="back-link">&larr; Back to all services</a>
    </div>
  </section>
'''
            + footer(root) + tail(root))


for s in SERVICES:
    path = os.path.join(OUT, "services", s["file"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(build_service(s))
    print("wrote services/" + s["file"])
print("service pages done")

# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------

SERVICE_CARDS = [
 ("services/ev-charging.html", "EV Charging Infrastructure",
  '<rect x="8" y="20" width="48" height="28" rx="4" stroke="currentColor" stroke-width="3"/><path d="M20 20V14a4 4 0 014-4h16a4 4 0 014 4v6" stroke="currentColor" stroke-width="3"/><path d="M28 32l4 8 8-16" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
 ("services/energy-storage.html", "Energy Storage",
  '<rect x="14" y="12" width="36" height="44" rx="4" stroke="currentColor" stroke-width="3"/><path d="M24 8h16" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><rect x="22" y="22" width="20" height="8" rx="1" fill="currentColor" opacity="0.3"/><rect x="22" y="34" width="20" height="8" rx="1" fill="currentColor" opacity="0.5"/><rect x="22" y="46" width="20" height="4" rx="1" fill="currentColor" opacity="0.7"/>'),
 ("services/commercial-solar.html", "Commercial Solar",
  '<circle cx="32" cy="32" r="10" stroke="currentColor" stroke-width="3"/><path d="M32 8v6M32 50v6M8 32h6M50 32h6M14.5 14.5l4.2 4.2M45.3 45.3l4.2 4.2M14.5 49.5l4.2-4.2M45.3 18.7l4.2-4.2" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'),
 ("services/om.html", "O&amp;M",
  '<rect x="10" y="16" width="44" height="32" rx="3" stroke="currentColor" stroke-width="3"/><path d="M10 28h44" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="40" r="3" fill="currentColor"/><path d="M28 40h18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>'),
 ("services/commissioning.html", "Commissioning",
  '<path d="M16 48V20l16-10 16 10v28" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/><path d="M28 48V34h8v14" stroke="currentColor" stroke-width="3"/><path d="M24 28l6 6 12-14" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
 ("services/smart-controls.html", "Smart Controls &amp; Energy Management",
  '<rect x="12" y="12" width="40" height="40" rx="4" stroke="currentColor" stroke-width="3"/><path d="M22 32h20M32 22v20" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="32" r="6" stroke="currentColor" stroke-width="2"/>'),
]

WHY = [
 ('<circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>',
  "Decades of combined field experience",
  "Deep practical knowledge across commercial energy construction, electrical systems, and complex site conditions."),
 ('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  "Safety-first culture",
  "OSHA and NFPA 70E compliance built into every phase of work, from planning through closeout."),
 ('<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
  "Fast, responsive mobilization",
  "Quick turnaround when schedules are tight and reliable response when needs arise in the field."),
 ('<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M9 15l2 2 4-4"/>',
  "Manufacturer-certified technicians",
  "Teams trained and credentialed by the equipment makers so installation and service remain warranty-compliant."),
 ('<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 010 7.75"/>',
  "Proven field leadership",
  "Experienced supervision and a reliable network of crews that deliver consistent quality on commercial sites."),
 ('<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>',
  "End-to-end accountability",
  "One team responsible from installation through commissioning and ongoing support."),
]

MARKETS = [
 ('<path d="M4 21V8l4-3 4 3v13M12 21V10l4-3 4 3v11M2 21h20M7 12h2M7 15h2M15 13h2M15 16h2"/>',
  "Multifamily",
  "EV charging for apartment communities and mixed-use properties, including retrofits in occupied buildings and structured parking."),
 ('<path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M12 9.5v5M9.5 12h5"/>',
  "Healthcare &amp; Institutional",
  "Charging and electrical infrastructure for medical campuses, research facilities, and public institutions, including phased work in active parking structures."),
 ('<path d="M2 20h20M5 20V8h4v12M10 20V4h4v16M15 20v-8h4v8"/>',
  "Commercial &amp; Retail",
  "Solar, storage, and charging for office campuses, retail sites, and hospitality properties, from service upgrades through commissioning."),
 ('<rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 3v5h-7V8zM6 16h2M15 16h2"/>',
  "Industrial &amp; Fleet",
  "Depot charging and supporting power for delivery and service fleets, including load management to avoid service upgrades."),
]

PROCESS = [
 ('<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><circle cx="11" cy="14" r="2"/><line x1="12.5" y1="15.5" x2="15" y2="18"/>',
  "Evaluate", "Site review, goals and existing conditions."),
 ('<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
  "Coordinate", "Utility, engineering and permitting."),
 ('<path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>',
  "Build", "Safe and compliant field execution."),
 ('<path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
  "Commission", "Testing, startup and QA/QC."),
 ('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  "Support", "Monitoring, O&amp;M and corrective."),
]


def build_index():
    root = ""
    svc = "".join(f'''          <a href="{href}" class="service-card">
            <div class="service-icon">
              <svg viewBox="0 0 64 64" fill="none">{svg}</svg>
            </div>
            <h3>{name}</h3>
          </a>
''' for href, name, svg in SERVICE_CARDS)

    def cards(rows, dark=False):
        cls = "card dark" if dark else "card"
        return "".join(f'''          <article class="{cls}">
            <div class="card-header">
              <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{svg}</svg></div>
              <h3>{title}</h3>
            </div>
            <p>{body}</p>
          </article>
''' for svg, title, body in rows)

    steps = "".join(f'''          <div class="step">
            <div class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>
            </div>
            <div class="step-text">
              <strong>{name}</strong>
              <span>{body}</span>
            </div>
          </div>
''' for svg, name, body in PROCESS)

    return (head("EcoBuilders | EV Charging, Solar, Energy Storage &amp; O&amp;M",
                 "EcoBuilders delivers EV charging, solar, energy storage, commissioning, O&amp;M, and smart controls "
                 "for commercial clients across California and nationwide.", root)
        + header(root, root)
        + f'''
  <main id="home">
    <section class="hero">
      <div class="container hero-content">
        <div class="eyebrow">Commercial Renewable-Energy Construction</div>
        <h1>POWERING<br><span>NEXT GEN.</span></h1>
        <p>EcoBuilders builds energy infrastructure,<br>commissioning, monitoring, and smart controls<br>for commercial clients nationwide.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{MAIL}">Request a Proposal</a>
          <a class="btn btn-outline" href="#services">Explore Capabilities</a>
        </div>
        <div class="hero-trust">
          <div>
            <strong>B-General Building</strong>
            <span class="trust-license">License #889419</span>
            <span>Commercial construction capability</span>
          </div>
          <div>
            <strong>C-10 Electrical</strong>
            <span>Licensed electrical contracting</span>
          </div>
          <div>
            <strong>C-46 Solar</strong>
            <span>Solar contractor classification</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="services">
      <div class="container">
        <div class="section-head centered">
          <div>
            <div class="eyebrow">What We Do</div>
            <h2>Integrated project delivery</h2>
          </div>
        </div>
        <div class="services-grid">
{svc}        </div>
      </div>
    </section>

    <section class="section section-dark" id="about">
      <div class="container">
        <div class="section-head">
          <div>
            <div class="eyebrow">Why EcoBuilders</div>
            <h2>What we bring to every project</h2>
          </div>
        </div>
        <div class="grid-3">
{cards(WHY, dark=True)}        </div>
      </div>
    </section>

    <section class="section" id="markets">
      <div class="container">
        <div class="section-head">
          <div>
            <div class="eyebrow">Markets Served</div>
            <h2>Commercial infrastructure at every scale</h2>
          </div>
        </div>
        <div class="grid-4">
{cards(MARKETS)}        </div>
      </div>
    </section>

    <section class="section section-dark" id="process">
      <div class="container">
        <div class="section-head">
          <div>
            <div class="eyebrow">Our Process</div>
            <h2>From concept to reliable operation</h2>
          </div>
        </div>
        <div class="process">
{steps}        </div>
      </div>
    </section>

    <section class="section" id="contact">
      <div class="container">
        <div class="section-head">
          <div>
            <div class="eyebrow">Contact EcoBuilders</div>
            <h2>Let's discuss your next project.</h2>
          </div>
        </div>
        <div class="contact-grid">
          <div class="contact-card">
            <p><strong>Noah Schij</strong><br>Owner / Operator at EcoBuilders<br><span class="credential-line">LEED AP</span></p>
            <p><strong>Email:</strong><br><a href="mailto:info@buildecoenergy.com">info@buildecoenergy.com</a></p>
            <p><strong>Phone:</strong><br><button type="button" class="phone-reveal">Click to show number</button></p>
            <p>Seal Beach, California<br>Serving California and clients nationwide</p>
          </div>
          <div class="contact-card contact-icons">
            <div class="icon-grid">
              <div class="icon-item"><img src="assets/icon-yelp.png" alt="Yelp"></div>
              <div class="icon-item"><img src="assets/icon-leed-1.png" alt="LEED"></div>
              <div class="icon-item"><img src="assets/icon-leed-2.png" alt="USGBC"></div>
              <div class="icon-item"><img src="assets/icon-bbb.png" alt="BBB"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
'''
        + footer(root) + tail(root))


with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(build_index())
print("wrote index.html")
