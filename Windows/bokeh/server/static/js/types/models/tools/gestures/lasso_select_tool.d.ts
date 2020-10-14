import { SelectTool, SelectToolView } from "./select_tool";
import { CallbackLike1 } from "../../callbacks/callback";
import { PolyAnnotation } from "../../annotations/poly_annotation";
import { PolyGeometry } from "../../../core/geometry";
import { PanEvent, KeyEvent } from "../../../core/ui_events";
import { Arrayable } from "../../../core/types";
import * as p from "../../../core/properties";
export declare class LassoSelectToolView extends SelectToolView {
    model: LassoSelectTool;
    protected data: {
        sx: number[];
        sy: number[];
    } | null;
    initialize(): void;
    connect_signals(): void;
    _active_change(): void;
    _keyup(ev: KeyEvent): void;
    _pan_start(ev: PanEvent): void;
    _pan(ev: PanEvent): void;
    _pan_end(ev: PanEvent): void;
    _clear_overlay(): void;
    _do_select(sx: number[], sy: number[], final: boolean, append: boolean): void;
    _emit_callback(geometry: PolyGeometry): void;
}
export declare namespace LassoSelectTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = SelectTool.Props & {
        select_every_mousemove: p.Property<boolean>;
        callback: p.Property<CallbackLike1<LassoSelectTool, {
            geometry: PolyGeometry & {
                x: Arrayable<number>;
                y: Arrayable<number>;
            };
        }> | null>;
        overlay: p.Property<PolyAnnotation>;
    };
}
export interface LassoSelectTool extends LassoSelectTool.Attrs {
}
export declare class LassoSelectTool extends SelectTool {
    properties: LassoSelectTool.Props;
    overlay: PolyAnnotation;
    constructor(attrs?: Partial<LassoSelectTool.Attrs>);
    static init_LassoSelectTool(): void;
    tool_name: string;
    icon: string;
    event_type: "pan";
    default_order: number;
}
