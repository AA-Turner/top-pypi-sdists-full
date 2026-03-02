from enum import Enum

from ._entity import Entity

class AnalyticTypeId(Enum):
    """
    The analytic type ID.
    """
    Unknown: int = 0
    Rule: int = 1 # A Rule in security analytics refers to predefined criteria or
                  # conditions set to monitor, alert, or enforce policies, playing
                  # a crucial role in access control, threat detection, and regulatory
                  # compliance across security systems.
    Behavioral: int = 2 # Behavioral analytics focus on monitoring and analyzing user
                        # or system actions to identify deviations from established
                        # patterns, aiding in the detection of insider threats, fraud,
                        # and advanced persistent threats (APTs).
    Statistical: int = 3 # Statistical analytics pertains to analyzing data patterns and
                         # anomalies using statistical models to predict, detect, and
                         # respond to potential threats, enhancing overall security
                         # posture through informed decision-making.
    Fingerprinting: int = 5 # Fingerprinting is the technique of collecting detailed system
                            # data, including software versions and configurations, to enhance
                            # threat detection, data loss prevention (DLP), and endpoint
                            # detection and response (EDR) capabilities.
    Tagging: int = 6 # Tagging refers to the practice of assigning labels or identifiers to data,
                     # users, assets, or activities to monitor, control access, and facilitate
                     # incident response across various security domains such as DLP and EDR.
    Keyword_Match: int = 7 # Keyword Match involves scanning content for specific terms to
                           # identify sensitive information, potential threats, or policy
                           # violations, aiding in DLP and compliance monitoring.
    Regular_Expressions: int = 8 # Regular Expressions are used to define complex search patterns
                                 # for identifying, validating, and extracting specific data sets
                                 # or threats within digital content, enhancing DLP, EDR, and threat
                                 # detection mechanisms.
    Exact_Data_Match: int = 9 # Exact Data Match is a precise comparison technique used to detect the
                              # unauthorized use or exposure of specific, sensitive information, crucial
                              # for enforcing DLP policies and protecting against data breaches.
    Partial_Data_Match: int = 10 # Partial Data Match involves identifying instances where segments of
                                 # sensitive information or patterns match, facilitating nuanced DLP and
                                 # threat detection without requiring complete data conformity.
    Indexed_Data_Match: int = 11 # Indexed Data Match refers to comparing content against a pre-compiled
                                 # index of sensitive information to efficiently detect and prevent
                                 # unauthorized access or breaches, streamlining DLP and compliance efforts.
    Other: int = 99

class Analytic(Entity):
    """
    The Analytic object contains details about the analytic technique used to
    analyze and derive insights from the data or information that led to the
    creation of a finding or conclusion.
    """

    type_id: AnalyticTypeId # The analytic type ID.


    # Optional:
    category: str | None = None # The analytic category.
    desc: str | None = None # The description of the analytic that generated the finding.
    name: str | None = None # The name of the analytic that generated the finding.
    related_analytics: 'list[Analytic] | None' = None # Other analytics related to this analytic.
    type: str | None = None # The analytic type.
    uid: str | None = None # The unique identifier of the analytic that generated the finding.
    version: str | None = None # The analytic version. For example: `1.1`.
