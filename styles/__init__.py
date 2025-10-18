cat > styles/__init__.py << 'EOF'
from .responsive import get_responsive_css, get_theme_css
__all__ = ['get_responsive_css', 'get_theme_css']
EOF
