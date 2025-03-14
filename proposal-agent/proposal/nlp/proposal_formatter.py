from typing import Dict, Any, Optional, List
import re

class ProposalFormatter:
    """Simple tool for formatting and optimizing proposal content"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize proposal formatter"""
        self.config = config or {}
    
    def format_proposal(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format proposal content
        
        Args:
            proposal_data: Dictionary containing proposal information
            
        Returns:
            Updated proposal data with formatted content
        """
        
        formatted_proposal = proposal_data.copy()
        
        content = proposal_data.get("content", "")
        title = proposal_data.get("title", "")

        formatted_content = self._format_content(content, title)
        formatted_proposal["content"] = formatted_content

        if not title:
            formatted_proposal["title"] = self._extract_title(formatted_content)

        if "tags" not in formatted_proposal or not formatted_proposal["tags"]:
            formatted_proposal["tags"] = self._extract_tags(formatted_content)
        
        return formatted_proposal
    
    def _format_content(self, content: str, title: str) -> str:
        """
        Format proposal content
        
        Args:
            content: Original content
            title: Proposal title
            
        Returns:
            Formatted content
        """
        if not content:
            return ""
        
        lines = content.strip().split('\n')
        formatted_parts = []

        has_title = any(line.startswith('#') for line in lines[:3])
        if title and not has_title:
            formatted_parts.append(f"# {title}\n")

        sections = self._identify_sections(content)
        if sections:
            formatted_parts.append(self._format_sections(sections))
        else:
            formatted_parts.append(content)

        return "\n\n".join(formatted_parts).strip()
    
    def _identify_sections(self, content: str) -> Dict[str, str]:
        """
        Try to identify different sections in the content
        
        Args:
            content: Proposal content
            
        Returns:
            Mapping of sections
        """
        sections = {}
        current_section = "main"
        current_content = []

        for line in content.split('\n'):
            if re.match(r'^#{1,3}\s+', line):
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                    current_content = []

                section_name = re.sub(r'^#{1,3}\s+', '', line).lower()
                current_section = section_name
            else:
                current_content.append(line)

        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _format_sections(self, sections: Dict[str, str]) -> str:
        """
        Format identified sections
        
        Args:
            sections: Section mapping
            
        Returns:
            Formatted content
        """
        formatted_content = []

        if "main" in sections:
            formatted_content.append(sections["main"])
            del sections["main"]

        priority_sections = [
            ("background", "background", "Background"),
            ("goals", "goals", "Goals"),
            ("content", "content", "Main Content"),
            ("suggestions", "suggestions", "Suggestions"),
            ("analysis", "analysis", "Analysis"),
            ("conclusion", "conclusion", "Conclusion")
        ]
        
        for keywords, section_key, title in priority_sections:
            section_content = None
            for key in sections:
                if any(kw in key for kw in keywords.split('|')):
                    section_content = sections[key]
                    del sections[key]
                    break

            if section_content:
                formatted_content.append(f"## {title}\n\n{section_content}")

        for title, content in sections.items():
            proper_title = title.capitalize()
            formatted_content.append(f"## {proper_title}\n\n{content}")
        
        return "\n\n".join(formatted_content)
    
    def _extract_title(self, content: str) -> str:
        """
        Extract title from content
        
        Args:
            content: Proposal content
            
        Returns:
            Extracted title
        """
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

        lines = content.strip().split('\n')
        if lines:
            return lines[0].strip()[:50]  # Limit length
        
        return "Proposal"
    
    def _extract_tags(self, content: str) -> List[str]:
        """
        Extract possible tags from content
        
        Args:
            content: Proposal content
            
        Returns:
            List of extracted tags
        """
        keywords = {
            "budget|funds|cost": "Finance",
            "community|residents": "Community",
            "environment|green": "Environment",
            "education|learning": "Education",
            "safety|security": "Safety",
            "facilities|construction": "Infrastructure",
            "activities|culture": "Activities"
        }
        
        found_tags = set()
        content_lower = content.lower()

        for kw_group, tag in keywords.items():
            if any(kw in content_lower for kw in kw_group.split('|')):
                found_tags.add(tag)

        if not found_tags:
            found_tags.add("General")
        
        return list(found_tags)