"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const signaling_1 = require("../../core/signaling");
const projections_1 = require("../../core/util/projections");
const plot_canvas_1 = require("./plot_canvas");
const gmaps_ready = new signaling_1.Signal0({}, "gmaps_ready");
const load_google_api = function (api_key) {
    window._bokeh_gmaps_callback = () => gmaps_ready.emit();
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = `https://maps.googleapis.com/maps/api/js?v=3.36&key=${api_key}&callback=_bokeh_gmaps_callback`;
    document.body.appendChild(script);
};
class GMapPlotView extends plot_canvas_1.PlotView {
    initialize() {
        this.pause();
        super.initialize();
        this._tiles_loaded = false;
        this.zoom_count = 0;
        const { zoom, lat, lng } = this.model.map_options;
        this.initial_zoom = zoom;
        this.initial_lat = lat;
        this.initial_lng = lng;
        this.canvas_view.map_el.style.position = "absolute";
        if (typeof google === "undefined" || google.maps == null) {
            if (typeof window._bokeh_gmaps_callback === "undefined") {
                load_google_api(this.model.api_key);
            }
            gmaps_ready.connect(() => this.request_render());
        }
        this.unpause();
    }
    update_range(range_info) {
        // RESET -------------------------
        if (range_info == null) {
            this.map.setCenter({ lat: this.initial_lat, lng: this.initial_lng });
            this.map.setOptions({ zoom: this.initial_zoom });
            super.update_range(null);
            // PAN ----------------------------
        }
        else if (range_info.sdx != null || range_info.sdy != null) {
            this.map.panBy(range_info.sdx || 0, range_info.sdy || 0);
            super.update_range(range_info);
            // ZOOM ---------------------------
        }
        else if (range_info.factor != null) {
            // The zoom count decreases the sensitivity of the zoom. (We could make this user configurable)
            let zoom_change;
            if (this.zoom_count !== 10) {
                this.zoom_count += 1;
                return;
            }
            this.zoom_count = 0;
            this.pause();
            super.update_range(range_info);
            if (range_info.factor < 0)
                zoom_change = -1;
            else
                zoom_change = 1;
            const old_map_zoom = this.map.getZoom();
            const new_map_zoom = old_map_zoom + zoom_change;
            // Zooming out too far causes problems
            if (new_map_zoom >= 2) {
                this.map.setZoom(new_map_zoom);
                // Check we haven't gone out of bounds, and if we have undo the zoom
                const [proj_xstart, proj_xend, ,] = this._get_projected_bounds();
                if (proj_xend - proj_xstart < 0) {
                    this.map.setZoom(old_map_zoom);
                }
            }
            this.unpause();
        }
        // Finally re-center
        this._set_bokeh_ranges();
    }
    _build_map() {
        const { maps } = google;
        this.map_types = {
            satellite: maps.MapTypeId.SATELLITE,
            terrain: maps.MapTypeId.TERRAIN,
            roadmap: maps.MapTypeId.ROADMAP,
            hybrid: maps.MapTypeId.HYBRID,
        };
        const mo = this.model.map_options;
        const map_options = {
            center: new maps.LatLng(mo.lat, mo.lng),
            zoom: mo.zoom,
            disableDefaultUI: true,
            mapTypeId: this.map_types[mo.map_type],
            scaleControl: mo.scale_control,
            tilt: mo.tilt,
        };
        if (mo.styles != null)
            map_options.styles = JSON.parse(mo.styles);
        // create the map with above options in div
        this.map = new maps.Map(this.canvas_view.map_el, map_options);
        // update bokeh ranges whenever the map idles, which should be after most UI action
        maps.event.addListener(this.map, 'idle', () => this._set_bokeh_ranges());
        // also need an event when bounds change so that map resizes trigger renders too
        maps.event.addListener(this.map, 'bounds_changed', () => this._set_bokeh_ranges());
        maps.event.addListenerOnce(this.map, 'tilesloaded', () => this._render_finished());
        // wire up listeners so that changes to properties are reflected
        this.connect(this.model.properties.map_options.change, () => this._update_options());
        this.connect(this.model.map_options.properties.styles.change, () => this._update_styles());
        this.connect(this.model.map_options.properties.lat.change, () => this._update_center('lat'));
        this.connect(this.model.map_options.properties.lng.change, () => this._update_center('lng'));
        this.connect(this.model.map_options.properties.zoom.change, () => this._update_zoom());
        this.connect(this.model.map_options.properties.map_type.change, () => this._update_map_type());
        this.connect(this.model.map_options.properties.scale_control.change, () => this._update_scale_control());
        this.connect(this.model.map_options.properties.tilt.change, () => this._update_tilt());
    }
    _render_finished() {
        this._tiles_loaded = true;
        this.notify_finished();
    }
    has_finished() {
        return super.has_finished() && this._tiles_loaded === true;
    }
    _get_latlon_bounds() {
        const bounds = this.map.getBounds();
        const top_right = bounds.getNorthEast();
        const bottom_left = bounds.getSouthWest();
        const xstart = bottom_left.lng();
        const xend = top_right.lng();
        const ystart = bottom_left.lat();
        const yend = top_right.lat();
        return [xstart, xend, ystart, yend];
    }
    _get_projected_bounds() {
        const [xstart, xend, ystart, yend] = this._get_latlon_bounds();
        const [proj_xstart, proj_ystart] = projections_1.wgs84_mercator.forward([xstart, ystart]);
        const [proj_xend, proj_yend] = projections_1.wgs84_mercator.forward([xend, yend]);
        return [proj_xstart, proj_xend, proj_ystart, proj_yend];
    }
    _set_bokeh_ranges() {
        const [proj_xstart, proj_xend, proj_ystart, proj_yend] = this._get_projected_bounds();
        this.frame.x_range.setv({ start: proj_xstart, end: proj_xend });
        this.frame.y_range.setv({ start: proj_ystart, end: proj_yend });
    }
    _update_center(fld) {
        const c = this.map.getCenter().toJSON();
        c[fld] = this.model.map_options[fld];
        this.map.setCenter(c);
        this._set_bokeh_ranges();
    }
    _update_map_type() {
        this.map.setOptions({ mapTypeId: this.map_types[this.model.map_options.map_type] });
    }
    _update_scale_control() {
        this.map.setOptions({ scaleControl: this.model.map_options.scale_control });
    }
    _update_tilt() {
        this.map.setOptions({ tilt: this.model.map_options.tilt });
    }
    _update_options() {
        this._update_styles();
        this._update_center('lat');
        this._update_center('lng');
        this._update_zoom();
        this._update_map_type();
    }
    _update_styles() {
        this.map.setOptions({ styles: JSON.parse(this.model.map_options.styles) });
    }
    _update_zoom() {
        this.map.setOptions({ zoom: this.model.map_options.zoom });
        this._set_bokeh_ranges();
    }
    // this method is expected and called by PlotView.render
    _map_hook(_ctx, frame_box) {
        const [left, top, width, height] = frame_box;
        this.canvas_view.map_el.style.top = `${top}px`;
        this.canvas_view.map_el.style.left = `${left}px`;
        this.canvas_view.map_el.style.width = `${width}px`;
        this.canvas_view.map_el.style.height = `${height}px`;
        if (this.map == null && typeof google !== "undefined" && google.maps != null)
            this._build_map();
    }
    // this overrides the standard _paint_empty to make the inner canvas transparent
    _paint_empty(ctx, frame_box) {
        const ow = this.layout._width.value;
        const oh = this.layout._height.value;
        const [left, top, iw, ih] = frame_box;
        ctx.clearRect(0, 0, ow, oh);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(0, oh);
        ctx.lineTo(ow, oh);
        ctx.lineTo(ow, 0);
        ctx.lineTo(0, 0);
        ctx.moveTo(left, top);
        ctx.lineTo(left + iw, top);
        ctx.lineTo(left + iw, top + ih);
        ctx.lineTo(left, top + ih);
        ctx.lineTo(left, top);
        ctx.closePath();
        if (this.model.border_fill_color != null) {
            ctx.fillStyle = this.model.border_fill_color;
            ctx.fill();
        }
    }
}
exports.GMapPlotView = GMapPlotView;
GMapPlotView.__name__ = "GMapPlotView";
